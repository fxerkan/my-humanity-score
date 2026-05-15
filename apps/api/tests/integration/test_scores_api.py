"""Integration tests for /scores/* endpoints — requires real PostgreSQL.

Coverage:
- GET /scores/{username}        public, no auth required (AC #1)
- GET /scores/me/breakdown      auth required              (AC #2)
- POST /scores/me/recalculate   returns task_id            (AC #6)
- Ethics: raw hidden values never in responses             (AC #3)
- Hidden buckets use only allowed enum values              (AC #4)

Design note: ``/auth/register`` automatically creates a zero-score
``MHSScore`` row for every new user (score_level="awakening",
total_score=0).  Tests that need a non-default score update that row
using ``_upsert_score``.  Tests that verify "no score" behaviour are
therefore not applicable in this system design.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

import pytest
from httpx import AsyncClient
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from models.score import MHSScore
from schemas.score import CarbonBucket, ConsistencyBucket, NetworkEffect, ToxicityBucket

pytestmark = pytest.mark.asyncio

# ── Allowed bucket value sets ─────────────────────────────────────────────────

_CARBON_BUCKETS = {b.value for b in CarbonBucket}
_TOXICITY_BUCKETS = {b.value for b in ToxicityBucket}
_NETWORK_EFFECTS = {b.value for b in NetworkEffect}
_CONSISTENCY_BUCKETS = {b.value for b in ConsistencyBucket}

# ── Forbidden raw field names (must NEVER appear in any response body) ─────────

_FORBIDDEN_RAW_FIELDS = {
    "carbon_penalty",
    "toxicity_penalty",
    "network_multiplier",
    "consistency_multiplier",
    "geo_equity_multiplier",
    "carbon_kg_per_year",
    "toxicity_index",
    # Ethics: forbidden demographic features
    "religion",
    "ethnicity",
    "race",
    "gender",
    "sexual_orientation",
    "nationality",
    "language",
    "disability",
    "political_affiliation",
    "economic_status",
}

# ── Helpers ───────────────────────────────────────────────────────────────────


def _make_user(suffix: str) -> dict:
    """Return a unique user dict for a given test suffix."""
    return {
        "username": f"sc_{suffix}",
        "email": f"sc_{suffix}@example.com",
        "password": "SecurePass123!",
    }


async def _register_and_login(client: AsyncClient, user: dict) -> tuple[dict, str]:
    """Register a user and return (user_data, access_token)."""
    reg = await client.post("/auth/register", json=user)
    assert reg.status_code == 201, reg.text
    login = await client.post(
        "/auth/login",
        json={"email": user["email"], "password": user["password"]},
    )
    assert login.status_code == 200, login.text
    return reg.json(), login.json()["access_token"]


async def _upsert_score(
    db: AsyncSession,
    user_id: uuid.UUID,
    *,
    total_score: Decimal = Decimal("342.00"),
    score_level: str = "contributor",
    social_impact: Decimal = Decimal("180"),
    environmental: Decimal = Decimal("120"),
    knowledge_innovation: Decimal = Decimal("200"),
    economic_contribution: Decimal = Decimal("100"),
    cultural_artistic: Decimal = Decimal("80"),
    civic_political: Decimal = Decimal("100"),
    carbon_penalty: Decimal = Decimal("10"),
    toxicity_penalty: Decimal = Decimal("5"),
    network_multiplier: Decimal = Decimal("1.100"),
    consistency_multiplier: Decimal = Decimal("1.100"),
    geo_equity_multiplier: Decimal = Decimal("1.050"),
) -> None:
    """Update the auto-created MHSScore row for the given user.

    /auth/register always inserts a zero-score row.  We UPDATE it so the
    app's ``ORDER BY calculated_at DESC`` returns our test values.
    """
    await db.execute(
        update(MHSScore)
        .where(MHSScore.user_id == user_id)
        .values(
            total_score=total_score,
            score_level=score_level,
            social_impact=social_impact,
            environmental=environmental,
            knowledge_innovation=knowledge_innovation,
            economic_contribution=economic_contribution,
            cultural_artistic=cultural_artistic,
            civic_political=civic_political,
            carbon_penalty=carbon_penalty,
            toxicity_penalty=toxicity_penalty,
            network_multiplier=network_multiplier,
            consistency_multiplier=consistency_multiplier,
            geo_equity_multiplier=geo_equity_multiplier,
            calculated_at=datetime.utcnow(),
        )
    )
    await db.flush()


def _assert_no_forbidden_fields(data: dict) -> None:
    """Recursively assert that no forbidden raw-value field names appear."""
    for key, value in data.items():
        assert (
            key not in _FORBIDDEN_RAW_FIELDS
        ), f"Forbidden raw field '{key}' found in API response"
        if isinstance(value, dict):
            _assert_no_forbidden_fields(value)


# ── GET /scores/{username} (public) ───────────────────────────────────────────


async def test_public_score_returns_summary(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """AC #1 — GET /scores/{username} returns expected fields."""
    u = _make_user("pub_sum")
    user_data, _ = await _register_and_login(client, u)
    await _upsert_score(db_session, uuid.UUID(user_data["id"]))

    resp = await client.get(f"/scores/{u['username']}")
    assert resp.status_code == 200, resp.text

    data = resp.json()
    assert data["username"] == u["username"]
    assert "final_score" in data
    assert "level" in data
    assert "name" in data["level"]
    assert "emoji" in data["level"]
    assert "calculated_at" in data


async def test_public_score_no_auth_required(client: AsyncClient, db_session: AsyncSession) -> None:
    """AC #1 — No Authorization header needed for GET /scores/{username}."""
    u = _make_user("pub_noauth")
    user_data, _ = await _register_and_login(client, u)
    await _upsert_score(db_session, uuid.UUID(user_data["id"]))

    # Deliberately omit auth header
    resp = await client.get(f"/scores/{u['username']}")
    assert resp.status_code == 200


async def test_public_score_nonexistent_user_returns_404(client: AsyncClient) -> None:
    """GET /scores/{username} for unknown user returns 404."""
    resp = await client.get("/scores/definitely_unknown_user_xyzzy")
    assert resp.status_code == 404


async def test_public_score_new_user_has_zero_score(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """A newly registered user immediately has a score (zero awakening score)."""
    u = _make_user("pub_zero")
    await _register_and_login(client, u)
    # No upsert — registration auto-creates zero score
    resp = await client.get(f"/scores/{u['username']}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["final_score"] == 0.0
    assert data["level"]["name"] == "Awakening"


async def test_public_score_level_name_is_human_readable(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Level name in public response must be human-readable, not a slug."""
    u = _make_user("pub_level")
    user_data, _ = await _register_and_login(client, u)
    await _upsert_score(db_session, uuid.UUID(user_data["id"]), score_level="contributor")

    resp = await client.get(f"/scores/{u['username']}")
    assert resp.status_code == 200
    level = resp.json()["level"]
    # Must not be a raw slug — must be the human-readable name
    assert level["name"] == "Contributor"
    assert level["emoji"] == "💫"
    assert level["range"] == [250, 399]


async def test_public_score_no_forbidden_raw_fields(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """AC #3 — Raw hidden-factor fields must not appear in public score response."""
    u = _make_user("pub_noforbid")
    user_data, _ = await _register_and_login(client, u)
    await _upsert_score(db_session, uuid.UUID(user_data["id"]))

    resp = await client.get(f"/scores/{u['username']}")
    assert resp.status_code == 200
    _assert_no_forbidden_fields(resp.json())


# ── GET /scores/me/breakdown (auth required) ──────────────────────────────────


async def test_breakdown_requires_auth(client: AsyncClient) -> None:
    """AC #2 — GET /scores/me/breakdown without token returns 401."""
    resp = await client.get("/scores/me/breakdown")
    assert resp.status_code == 401


async def test_breakdown_with_invalid_token_returns_401(client: AsyncClient) -> None:
    """AC #2 — GET /scores/me/breakdown with invalid token returns 401."""
    resp = await client.get(
        "/scores/me/breakdown",
        headers={"Authorization": "Bearer invalid.token.here"},
    )
    assert resp.status_code == 401


async def test_breakdown_returns_full_categories(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """GET /scores/me/breakdown returns all 6 category entries."""
    u = _make_user("bkd_cats")
    user_data, token = await _register_and_login(client, u)
    await _upsert_score(db_session, uuid.UUID(user_data["id"]))

    resp = await client.get(
        "/scores/me/breakdown",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()

    expected_categories = {
        "social_impact",
        "environmental",
        "knowledge_innovation",
        "economic_contribution",
        "cultural_artistic",
        "civic_political",
    }
    assert set(data["categories"].keys()) == expected_categories


async def test_breakdown_new_user_returns_zero_score(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """A newly registered user's breakdown returns the zero awakening score."""
    u = _make_user("bkd_zero")
    _, token = await _register_and_login(client, u)
    # No upsert — use auto-created zero score
    resp = await client.get(
        "/scores/me/breakdown",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["final_score"] == 0.0
    assert data["level"]["name"] == "Awakening"


async def test_breakdown_category_weights_sum_to_one(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Category weights in breakdown must sum to 1.0."""
    u = _make_user("bkd_wts")
    user_data, token = await _register_and_login(client, u)
    await _upsert_score(db_session, uuid.UUID(user_data["id"]))

    resp = await client.get(
        "/scores/me/breakdown",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    categories = resp.json()["categories"]
    total_weight = sum(v["weight"] for v in categories.values())
    assert abs(total_weight - 1.0) < 1e-6, f"Weights sum to {total_weight}, expected 1.0"


async def test_breakdown_contribution_equals_score_times_weight(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Each category contribution must equal score * weight (to 2 decimal places)."""
    u = _make_user("bkd_contrib")
    user_data, token = await _register_and_login(client, u)
    await _upsert_score(db_session, uuid.UUID(user_data["id"]))

    resp = await client.get(
        "/scores/me/breakdown",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    for cat, detail in resp.json()["categories"].items():
        expected = round(detail["score"] * detail["weight"], 2)
        assert (
            abs(detail["contribution"] - expected) < 0.01
        ), f"{cat}: contribution {detail['contribution']} != score*weight {expected}"


async def test_breakdown_hidden_adjustments_use_allowed_buckets(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """AC #4 — Hidden adjustment buckets must use only allowed enum values."""
    u = _make_user("bkd_buckets")
    user_data, token = await _register_and_login(client, u)
    await _upsert_score(db_session, uuid.UUID(user_data["id"]))

    resp = await client.get(
        "/scores/me/breakdown",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    adj = resp.json()["hidden_adjustments"]

    assert adj["carbon_bucket"] in _CARBON_BUCKETS, f"Bad carbon_bucket: {adj['carbon_bucket']}"
    assert (
        adj["toxicity_bucket"] in _TOXICITY_BUCKETS
    ), f"Bad toxicity_bucket: {adj['toxicity_bucket']}"
    assert adj["network_effect"] in _NETWORK_EFFECTS, f"Bad network_effect: {adj['network_effect']}"
    assert adj["consistency"] in _CONSISTENCY_BUCKETS, f"Bad consistency: {adj['consistency']}"
    assert isinstance(adj["equity_boost"], bool), "equity_boost must be a boolean"


async def test_breakdown_no_forbidden_raw_fields(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """AC #3 — Raw hidden-factor fields must not appear in breakdown response."""
    u = _make_user("bkd_noforbid")
    user_data, token = await _register_and_login(client, u)
    await _upsert_score(db_session, uuid.UUID(user_data["id"]))

    resp = await client.get(
        "/scores/me/breakdown",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    _assert_no_forbidden_fields(resp.json())


async def test_breakdown_level_has_name_and_emoji(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Level in breakdown includes human-readable name and emoji."""
    u = _make_user("bkd_level")
    user_data, token = await _register_and_login(client, u)
    await _upsert_score(db_session, uuid.UUID(user_data["id"]), score_level="impact_maker")

    resp = await client.get(
        "/scores/me/breakdown",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    level = resp.json()["level"]
    assert level["name"] == "Impact Maker"
    assert level["emoji"] == "⭐"


# ── POST /scores/me/recalculate ───────────────────────────────────────────────


async def test_recalculate_requires_auth(client: AsyncClient) -> None:
    """POST /scores/me/recalculate without token returns 401."""
    resp = await client.post("/scores/me/recalculate")
    assert resp.status_code == 401


async def test_recalculate_returns_task_id_and_queued_status(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """AC #6 — POST /scores/me/recalculate returns task_id and status 'queued'."""
    u = _make_user("recalc_ok")
    _, token = await _register_and_login(client, u)

    resp = await client.post(
        "/scores/me/recalculate",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 202, resp.text
    data = resp.json()
    assert "task_id" in data
    assert data["task_id"], "task_id must not be empty"
    assert data["status"] == "queued"


async def test_recalculate_task_id_contains_user_id(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """Stub task_id should reference the requesting user for traceability."""
    u = _make_user("recalc_uid")
    user_data, token = await _register_and_login(client, u)

    resp = await client.post(
        "/scores/me/recalculate",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 202
    task_id = resp.json()["task_id"]
    # Stub format: "stub-{user_id}"
    assert user_data["id"] in task_id


# ── GET /scores/leaderboard (public) ─────────────────────────────────────────


async def test_leaderboard_is_public(client: AsyncClient) -> None:
    """GET /scores/leaderboard requires no authentication."""
    resp = await client.get("/scores/leaderboard")
    assert resp.status_code == 200


async def test_leaderboard_returns_list(client: AsyncClient) -> None:
    """GET /scores/leaderboard returns a JSON array."""
    resp = await client.get("/scores/leaderboard")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


# ── Global percentile ─────────────────────────────────────────────────────────


async def test_public_score_global_percentile_two_users(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    """With two users the higher scorer should have a percentile > 0."""
    u_a = _make_user("pct_a")
    u_b = _make_user("pct_b")
    data_a, _ = await _register_and_login(client, u_a)
    data_b, _ = await _register_and_login(client, u_b)

    await _upsert_score(
        db_session,
        uuid.UUID(data_a["id"]),
        total_score=Decimal("200.00"),
        score_level="rising_star",
    )
    await _upsert_score(
        db_session,
        uuid.UUID(data_b["id"]),
        total_score=Decimal("400.00"),
        score_level="impact_maker",
    )

    resp = await client.get(f"/scores/{u_b['username']}")
    assert resp.status_code == 200
    percentile = resp.json().get("global_percentile")
    assert percentile is not None
    assert percentile > 0  # user B scored higher than user A
