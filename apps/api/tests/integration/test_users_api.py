"""Integration tests for /users/* endpoints — requires real PostgreSQL."""

import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.asyncio

_USER = {
    "username": "user_api_tester",
    "email": "user_api@example.com",
    "password": "SecurePass123!",
}


async def _register_and_login(client: AsyncClient) -> tuple[dict, str]:
    """Helper: register a user and return (user_data, access_token)."""
    reg = await client.post("/auth/register", json=_USER)
    assert reg.status_code == 201
    login = await client.post(
        "/auth/login",
        json={"email": _USER["email"], "password": _USER["password"]},
    )
    return reg.json(), login.json()["access_token"]


async def test_get_me_returns_own_profile(client: AsyncClient) -> None:
    """GET /users/me with valid token returns the authenticated user's profile."""
    user_data, token = await _register_and_login(client)
    resp = await client.get(
        "/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == user_data["id"]
    assert data["email"] == _USER["email"]


async def test_get_me_unauthenticated_returns_401(client: AsyncClient) -> None:
    resp = await client.get("/users/me")
    assert resp.status_code == 401


async def test_update_me_changes_display_name(client: AsyncClient) -> None:
    _, token = await _register_and_login(client)
    resp = await client.patch(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"display_name": "Updated Name"},
    )
    assert resp.status_code == 200
    assert resp.json()["display_name"] == "Updated Name"


async def test_get_public_profile_by_username(client: AsyncClient) -> None:
    """GET /users/{username} is accessible without authentication."""
    await client.post("/auth/register", json=_USER)
    resp = await client.get(f"/users/{_USER['username']}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == _USER["username"]


async def test_get_nonexistent_user_returns_404(client: AsyncClient) -> None:
    resp = await client.get("/users/definitely_not_a_real_user_xyzzy")
    assert resp.status_code == 404
