"""JWT token creation and verification.

Password hashing uses the ``bcrypt`` library directly (passlib removed) to
avoid the passlib ≥1.7.4 / bcrypt ≥4.0 incompatibility (__about__ removed).

Passwords are SHA-256 pre-hashed before bcrypt so the 72-byte bcrypt limit
is never hit in practice (SHA-256 digest is always 64 hex chars = 64 bytes).
"""

import hashlib
from datetime import UTC, datetime, timedelta
from typing import Any

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

    Args:
        subject: The user UUID to embed as the ``sub`` claim.

    Returns:
        Encoded JWT string.
    """
    expire = datetime.now(UTC) + timedelta(
        days=settings.jwt_refresh_token_expire_days
    )
    payload: dict[str, Any] = {"sub": subject, "exp": expire, "type": "refresh"}
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
