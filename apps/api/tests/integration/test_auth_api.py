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


async def test_replay_attack_rejected(client: AsyncClient) -> None:
    """Used refresh token cannot be reused (replay protection)."""
    await client.post("/auth/register", json=_USER)
    login_resp = await client.post(
        "/auth/login",
        json={"email": _USER["email"], "password": _USER["password"]},
    )
    original_token = login_resp.json()["refresh_token"]

    # First use — should succeed
    first = await client.post("/auth/refresh", json={"refresh_token": original_token})
    assert first.status_code == 200

    # Second use of the same token — must be rejected
    second = await client.post("/auth/refresh", json={"refresh_token": original_token})
    assert second.status_code == 401


async def test_full_auth_flow(client: AsyncClient) -> None:
    """register → login → refresh → replay rejected → logout → post-logout refresh rejected."""
    # Register
    reg = await client.post("/auth/register", json=_USER)
    assert reg.status_code == 201

    # Login
    login_resp = await client.post(
        "/auth/login",
        json={"email": _USER["email"], "password": _USER["password"]},
    )
    assert login_resp.status_code == 200
    tokens = login_resp.json()
    original_refresh = tokens["refresh_token"]

    # Refresh — should return a new token pair
    refresh_resp = await client.post("/auth/refresh", json={"refresh_token": original_refresh})
    assert refresh_resp.status_code == 200
    new_tokens = refresh_resp.json()
    new_refresh = new_tokens["refresh_token"]
    assert new_refresh != original_refresh

    # Replay: old refresh token must now be rejected
    replay = await client.post("/auth/refresh", json={"refresh_token": original_refresh})
    assert replay.status_code == 401

    # Logout using the new token
    logout_resp = await client.post("/auth/logout", json={"refresh_token": new_refresh})
    assert logout_resp.status_code == 200

    # After logout, the new refresh token must also be rejected
    after_logout = await client.post("/auth/refresh", json={"refresh_token": new_refresh})
    assert after_logout.status_code == 401


async def test_logout_is_idempotent(client: AsyncClient) -> None:
    """Logging out twice with the same token must not raise an error."""
    await client.post("/auth/register", json=_USER)
    login_resp = await client.post(
        "/auth/login",
        json={"email": _USER["email"], "password": _USER["password"]},
    )
    refresh_token = login_resp.json()["refresh_token"]

    resp1 = await client.post("/auth/logout", json={"refresh_token": refresh_token})
    assert resp1.status_code == 200

    # Second logout with same token — should still return 200
    resp2 = await client.post("/auth/logout", json={"refresh_token": refresh_token})
    assert resp2.status_code == 200
