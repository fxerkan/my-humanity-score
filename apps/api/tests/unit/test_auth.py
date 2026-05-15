"""Unit tests for auth utilities — no database required."""

import time

import pytest
from jose import jwt

from core.config import settings
from core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)

# ── Password hashing ──────────────────────────────────────────────────────────


def test_hash_password_returns_bcrypt_hash() -> None:
    h = hash_password("secret123")
    assert h.startswith("$2b$") or h.startswith("$2a$")


def test_verify_password_correct() -> None:
    plain = "myS3cur3Pass!"
    assert verify_password(plain, hash_password(plain)) is True


def test_verify_password_wrong() -> None:
    assert verify_password("wrongpass", hash_password("rightpass")) is False


def test_hash_different_for_same_input() -> None:
    """bcrypt uses random salt — two hashes of the same string differ."""
    h1 = hash_password("same")
    h2 = hash_password("same")
    assert h1 != h2


# ── JWT access token ──────────────────────────────────────────────────────────


def test_create_access_token_returns_string() -> None:
    token = create_access_token("user-abc")
    assert isinstance(token, str)
    assert len(token) > 0


def test_decode_access_token_returns_subject() -> None:
    user_id = "user-123"
    token = create_access_token(user_id)
    payload = decode_token(token)
    assert payload["sub"] == user_id
    assert payload["type"] == "access"


def test_access_token_has_expiry() -> None:
    token = create_access_token("u1")
    payload = decode_token(token)
    assert "exp" in payload
    assert payload["exp"] > time.time()


# ── JWT refresh token ─────────────────────────────────────────────────────────


def test_create_refresh_token_type_is_refresh() -> None:
    token = create_refresh_token("user-xyz")
    payload = decode_token(token)
    assert payload["type"] == "refresh"


def test_refresh_token_longer_expiry_than_access() -> None:
    access = create_access_token("u1")
    refresh = create_refresh_token("u1")
    access_exp = decode_token(access)["exp"]
    refresh_exp = decode_token(refresh)["exp"]
    assert refresh_exp > access_exp


# ── Expired / tampered token rejection ───────────────────────────────────────


def test_decode_invalid_token_raises() -> None:
    with pytest.raises(ValueError, match="Invalid token"):
        decode_token("not.a.valid.jwt")


def test_decode_tampered_signature_raises() -> None:
    token = create_access_token("u1")
    tampered = token[:-5] + "XXXXX"
    with pytest.raises(ValueError, match="Invalid token"):
        decode_token(tampered)


def test_decode_expired_token_raises() -> None:
    from datetime import UTC, datetime, timedelta

    payload = {"sub": "u1", "exp": datetime.now(UTC) - timedelta(seconds=1), "type": "access"}
    expired = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    with pytest.raises(ValueError, match="Invalid token"):
        decode_token(expired)
