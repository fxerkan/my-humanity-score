"""Authentication endpoints: register, login, refresh, logout, me."""

import redis.asyncio as redis
from fastapi import APIRouter, Depends, HTTPException, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.database import get_db
from core.redis_client import get_redis_dep
from core.security import (
    consume_refresh_token,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    invalidate_refresh_token,
    store_refresh_token,
    verify_password,
)
from models.score import MHSScore
from models.user import User
from schemas.user import LoginRequest, RefreshRequest, TokenResponse, UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])

_REFRESH_TTL = settings.jwt_refresh_token_expire_days * 86400

limiter = Limiter(key_func=get_remote_address)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(body: UserCreate, db: AsyncSession = Depends(get_db)) -> User:
    """Register a new user and atomically create their MHS score row.

    Args:
        body: Registration payload containing username, email, and password.
        db: Injected async database session.

    Returns:
        The newly created User ORM object.

    Raises:
        HTTPException 409: If email or username is already taken.
    """
    existing = await db.scalar(select(User).where(User.email == body.email))
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    existing_username = await db.scalar(select(User).where(User.username == body.username))
    if existing_username:
        raise HTTPException(status_code=409, detail="Username already taken")

    user = User(
        username=body.username,
        email=body.email,
        hashed_password=hash_password(body.password),
    )
    db.add(user)
    # Flush to obtain user.id before creating the dependent score row.
    await db.flush()

    score = MHSScore(user_id=user.id)
    db.add(score)

    await db.commit()
    await db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
@limiter.limit("20/minute")
async def login(
    request: Request,
    body: LoginRequest,
    db: AsyncSession = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis_dep),
) -> dict:
    """Authenticate a user and return a JWT access/refresh token pair.

    The refresh token JTI is stored in Redis to enable rotation and invalidation.

    Args:
        body: Login payload with email and password.
        db: Injected async database session.
        redis_client: Injected async Redis client.

    Returns:
        Dict with ``access_token`` and ``refresh_token``.

    Raises:
        HTTPException 401: For any invalid credentials (no email enumeration).
        HTTPException 403: If the account is disabled.
    """
    user = await db.scalar(select(User).where(User.email == body.email))
    if (
        not user
        or not user.hashed_password
        or not verify_password(body.password, user.hashed_password)
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is disabled")

    refresh_token = create_refresh_token(str(user.id))
    payload = decode_token(refresh_token)
    jti: str = payload["jti"]
    await store_refresh_token(redis_client, jti, str(user.id), _REFRESH_TTL)

    return {
        "access_token": create_access_token(str(user.id)),
        "refresh_token": refresh_token,
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    body: RefreshRequest,
    redis_client: redis.Redis = Depends(get_redis_dep),
) -> dict:
    """Rotate a refresh token: invalidate the old one, issue a new pair.

    Args:
        body: Payload containing the current refresh token.
        redis_client: Injected async Redis client.

    Returns:
        Dict with new ``access_token`` and ``refresh_token``.

    Raises:
        HTTPException 401: If the token is invalid, expired, or already used.
    """
    try:
        payload = decode_token(body.refresh_token)
        if payload.get("type") != "refresh":
            raise ValueError("Not a refresh token")
        jti: str | None = payload.get("jti")
        user_id: str = payload["sub"]
        if not jti or not await consume_refresh_token(redis_client, jti):
            raise ValueError("Token already used or expired")
    except (ValueError, KeyError):
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Issue a new token pair and register the new refresh JTI.
    new_refresh = create_refresh_token(user_id)
    new_payload = decode_token(new_refresh)
    new_jti: str = new_payload["jti"]
    await store_refresh_token(redis_client, new_jti, user_id, _REFRESH_TTL)

    return {
        "access_token": create_access_token(user_id),
        "refresh_token": new_refresh,
    }


@router.post("/logout", status_code=200)
async def logout(
    body: RefreshRequest,
    redis_client: redis.Redis = Depends(get_redis_dep),
) -> dict:
    """Invalidate a refresh token, effectively logging the user out.

    Idempotent: already-expired or unknown tokens are silently ignored.

    Args:
        body: Payload containing the refresh token to invalidate.
        redis_client: Injected async Redis client.

    Returns:
        A confirmation message dict.
    """
    try:
        payload = decode_token(body.refresh_token)
        jti = payload.get("jti")
        if jti:
            await invalidate_refresh_token(redis_client, jti)
    except ValueError:
        pass  # Already invalid or expired — that's fine.
    return {"message": "logged out"}
