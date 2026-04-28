"""JWT token creation and verification.

Password hashing uses the ``bcrypt`` library directly (passlib removed) to
avoid the passlib ≥1.7.4 / bcrypt ≥4.0 incompatibility (__about__ removed).

Passwords are SHA-256 pre-hashed before bcrypt so the 72-byte bcrypt limit
is never hit in practice (SHA-256 digest is always 64 hex chars = 64 bytes).
"""

import hashlib
import uuid
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import redis.asyncio as redis

import bcrypt
from jose import JWTError, jwt

from core.config import settings

_ENCODING = "utf-8"


def _prehash(plain: str) -> bytes:
    """Return SHA-256 hex digest of *plain* as bytes (always 64 bytes).

    Args:
        plain: Plain-text input string.

    Returns:
        64-byte SHA-256 hex digest encoded as UTF-8.
    """
    return hashlib.sha256(plain.encode(_ENCODING)).hexdigest().encode(_ENCODING)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain-text password against a stored bcrypt hash.

    Args:
        plain: The password entered by the user.
        hashed: The stored bcrypt hash string (``$2b$...``).

    Returns:
        True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(_prehash(plain), hashed.encode(_ENCODING))


def hash_password(plain: str) -> str:
    """Hash a plain-text password with bcrypt (work factor 12).

    Args:
        plain: The plain-text password.

    Returns:
        A ``$2b$...`` bcrypt hash string.
    """
    return bcrypt.hashpw(_prehash(plain), bcrypt.gensalt(rounds=12)).decode(_ENCODING)


def create_access_token(subject: str, extra: dict[str, Any] | None = None) -> str:
    """Create a short-lived JWT access token.

    Args:
        subject: The user UUID to embed as the ``sub`` claim.
        extra: Optional additional claims to merge into the payload.

    Returns:
        Encoded JWT string.
    """
    expire = datetime.now(UTC) + timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )
    payload: dict[str, Any] = {"sub": subject, "exp": expire, "type": "access"}
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def create_refresh_token(subject: str) -> str:
    """Create a long-lived JWT refresh token.

    A unique ``jti`` (JWT ID) claim is included so that two tokens issued for
    the same subject within the same second produce different encoded strings,
    enabling reliable token-rotation equality checks.

    Args:
        subject: The user UUID to embed as the ``sub`` claim.

    Returns:
        Encoded JWT string.
    """
    expire = datetime.now(UTC) + timedelta(
        days=settings.jwt_refresh_token_expire_days
    )
    payload: dict[str, Any] = {
        "sub": subject,
        "exp": expire,
        "type": "refresh",
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT token.

    Args:
        token: Encoded JWT string.

    Returns:
        Decoded payload dict.

    Raises:
        ValueError: If the token is invalid, expired, or tampered.
    """
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise ValueError("Invalid token") from exc


# ── Redis-based refresh-token helpers ────────────────────────────────────────

REFRESH_TOKEN_PREFIX = "refresh:"


def _token_key(jti: str) -> str:
    """Return the Redis key for a refresh token JTI.

    Args:
        jti: The JWT ID claim value.

    Returns:
        Namespaced Redis key string.
    """
    return f"{REFRESH_TOKEN_PREFIX}{jti}"


async def store_refresh_token(
    redis_client: "redis.Redis",
    jti: str,
    user_id: str,
    ttl_seconds: int,
) -> None:
    """Persist a refresh token JTI in Redis with a TTL.

    Args:
        redis_client: Async Redis client instance.
        jti: Unique JWT ID from the token payload.
        user_id: UUID string of the owning user.
        ttl_seconds: Lifetime in seconds after which Redis auto-expires the key.
    """
    await redis_client.setex(_token_key(jti), ttl_seconds, user_id)


async def invalidate_refresh_token(
    redis_client: "redis.Redis",
    jti: str,
) -> None:
    """Remove a refresh token JTI from Redis (immediate invalidation).

    Args:
        redis_client: Async Redis client instance.
        jti: Unique JWT ID to invalidate.
    """
    await redis_client.delete(_token_key(jti))


async def is_refresh_token_valid(
    redis_client: "redis.Redis",
    jti: str,
) -> bool:
    """Check whether a refresh token JTI is still valid.

    Args:
        redis_client: Async Redis client instance.
        jti: Unique JWT ID to check.

    Returns:
        True if the JTI exists in Redis (not yet used/invalidated).
    """
    return await redis_client.exists(_token_key(jti)) == 1


# Lua script for atomic check-and-delete (prevents TOCTOU race on refresh).
_LUA_CONSUME = """
if redis.call('EXISTS', KEYS[1]) == 1 then
    return redis.call('DEL', KEYS[1])
else
    return 0
end
"""


async def consume_refresh_token(
    redis_client: "redis.Redis",
    jti: str,
) -> bool:
    """Atomically check existence and delete a refresh token JTI.

    Uses a Lua script so that two concurrent requests with the same token
    cannot both pass the existence check under multiple replicas.

    Args:
        redis_client: Async Redis client instance.
        jti: Unique JWT ID to consume.

    Returns:
        True if the token existed (was valid), False if already used/expired.
    """
    result = await redis_client.eval(_LUA_CONSUME, 1, _token_key(jti))
    return bool(result)
