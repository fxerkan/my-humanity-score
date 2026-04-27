"""Integration tests for the /auth/* endpoints — requires real PostgreSQL."""

import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.asyncio


_USER = {
    "username": "auth_test_user",
    "email": "auth_test@example.com",
    "password": "SecurePass123!",
}


async def test_register_creates_user(client: AsyncClient) -> None:
    """POST /auth/register returns 201 and user payload."""
    resp = await client.post("/auth/register", json=_USER)
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == _USER["email"]
    assert data["username"] == _USER["username"]
    assert "id" in data
    assert "hashed_password" not in data  # never exposed


async def test_register_duplicate_email_returns_409(client: AsyncClient) -> None:
    await client.post("/auth/register", json=_USER)
    resp = await client.post("/auth/register", json=_USER)
    assert resp.status_code == 409


async def test_login_returns_tokens(client: AsyncClient) -> None:
    await client.post("/auth/register", json=_USER)
    resp = await client.post(
        "/auth/login",
        json={"email": _USER["email"], "password": _USER["password"]},
    )
    assert resp.status_code == 200
    tokens = resp.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens


async def test_login_wrong_password_returns_401(client: AsyncClient) -> None:
    await client.post("/auth/register", json=_USER)
    resp = await client.post(
        "/auth/login",
        json={"email": _USER["email"], "password": "WrongPassword!"},
    )
    assert resp.status_code == 401


async def test_login_unknown_email_returns_401(client: AsyncClient) -> None:
    """Login with non-existent email must return 401, not 404 (no user enumeration)."""
    resp = await client.post(
        "/auth/login",
        json={"email": "nobody@example.com", "password": "whatever"},
    )
    assert resp.status_code == 401


async def test_refresh_returns_new_tokens(client: AsyncClient) -> None:
    await client.post("/auth/register", json=_USER)
    login = await client.post(
        "/auth/login",
        json={"email": _USER["email"], "password": _USER["password"]},
    )
    refresh_token = login.json()["refresh_token"]

    resp = await client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert resp.status_code == 200
    new_tokens = resp.json()
    assert "access_token" in new_tokens
    # New refresh token should differ from the old one
    assert new_tokens["refresh_token"] != refresh_token


async def test_refresh_with_access_token_returns_401(client: AsyncClient) -> None:
    """Using an access token as a refresh token must be rejected."""
    await client.post("/auth/register", json=_USER)
    login = await client.post(
        "/auth/login",
        json={"email": _USER["email"], "password": _USER["password"]},
    )
    access_token = login.json()["access_token"]

    resp = await client.post("/auth/refresh", json={"refresh_token": access_token})
    assert resp.status_code == 401
