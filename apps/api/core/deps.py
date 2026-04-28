"""FastAPI dependency injection: auth, DB session."""

import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.security import decode_token
from models.user import User

bearer = HTTPBearer(auto_error=False)


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> uuid.UUID:
    """Extract and validate the authenticated user's UUID from a bearer token.

    Args:
        credentials: HTTP Authorization header parsed by FastAPI's HTTPBearer.

    Returns:
        The authenticated user's UUID.

    Raises:
        HTTPException 401: If no token is provided or the token is invalid.
    """
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        payload = decode_token(credentials.credentials)
        if payload.get("type") != "access":
            raise ValueError("Wrong token type")
        return uuid.UUID(payload["sub"])
    except (ValueError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )


async def get_optional_user_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> uuid.UUID | None:
    """Extract the authenticated user's UUID if a valid token is present.

    Unlike ``get_current_user_id``, this dependency never raises; it returns
    ``None`` for unauthenticated requests or requests with invalid tokens.

    Args:
        credentials: HTTP Authorization header parsed by FastAPI's HTTPBearer.

    Returns:
        The authenticated user's UUID, or ``None``.
    """
    if not credentials:
        return None
    try:
        payload = decode_token(credentials.credentials)
        return uuid.UUID(payload["sub"])
    except Exception:
        return None


async def get_current_user(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> "User":
    """Resolve the authenticated user UUID to a full User ORM object.

    Args:
        user_id: UUID resolved by ``get_current_user_id``.
        db: Injected async database session.

    Returns:
        The User ORM instance for the authenticated user.

    Raises:
        HTTPException 401: If the user no longer exists in the database.
    """
    user = await db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
