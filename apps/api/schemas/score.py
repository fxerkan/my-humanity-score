"""MHS score response schemas.

Public surface:
- ScoreResponse: raw ORM-level schema (used by /users/me/score)
- ScoreSummary: embedded in UserPublicResponse
- ScorePublic: public GET /scores/{username} response
- CategoryDetail: per-category score/weight/contribution
- HiddenAdjustments: client-safe bucket labels only (no raw values)
- BreakdownResponse: authenticated GET /scores/me/breakdown response
- RecalculateResponse: POST /scores/me/recalculate response

Ethics rule: raw hidden-factor values (carbon_kg, toxicity_index,
penalty amounts, multiplier floats) MUST NEVER appear in any response.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field

# ── Allowed enum values for hidden adjustment buckets ────────────────────────

class CarbonBucket(str, Enum):
    """Client-safe carbon footprint bucket.  Raw kg CO2 values are never exposed."""

    none = "none"
    low = "low"
    medium = "medium"
    high = "high"


class ToxicityBucket(str, Enum):
    """Client-safe toxicity bucket.  Raw toxicity index is never exposed."""

    clean = "clean"
    caution = "caution"
    warning = "warning"


class NetworkEffect(str, Enum):
    """Client-safe network multiplier bucket."""

    none = "none"
    positive = "positive"
    strong = "strong"


class ConsistencyBucket(str, Enum):
    """Client-safe consistency multiplier bucket."""

    irregular = "irregular"
    regular = "regular"
    consistent = "consistent"


# ── Level metadata ────────────────────────────────────────────────────────────

LEVEL_METADATA: dict[str, dict] = {
    "awakening":           {"name": "Awakening",          "emoji": "🌱", "range": [0, 99]},
    "rising_star":         {"name": "Rising Star",         "emoji": "🌟", "range": [100, 249]},
    "contributor":         {"name": "Contributor",         "emoji": "💫", "range": [250, 399]},
    "impact_maker":        {"name": "Impact Maker",        "emoji": "⭐", "range": [400, 549]},
    "change_agent":        {"name": "Change Agent",        "emoji": "🏆", "range": [550, 699]},
    "humanity_champion":   {"name": "Humanity Champion",   "emoji": "🌍", "range": [700, 849]},
    "humanity_legend":     {"name": "Humanity Legend",     "emoji": "👑", "range": [850, 1000]},
}


def level_info(slug: str) -> dict:
    """Return name/emoji/range dict for a level slug.

    Args:
        slug: Level slug string, e.g. ``"contributor"``.

    Returns:
        Dict with ``name``, ``emoji``, and ``range`` keys.
    """
    return LEVEL_METADATA.get(slug, {"name": slug, "emoji": "", "range": [0, 1000]})


# ── Helper: map ORM multiplier floats to client-safe buckets ──────────────────

def _network_bucket(multiplier: Decimal) -> NetworkEffect:
    """Convert a raw network multiplier to a client-safe enum bucket.

    Args:
        multiplier: The stored network_multiplier Decimal value.

    Returns:
        Client-safe ``NetworkEffect`` bucket.
    """
    f = float(multiplier)
    if f >= 1.3:
        return NetworkEffect.strong
    if f > 1.0:
        return NetworkEffect.positive
    return NetworkEffect.none


def _consistency_bucket(multiplier: Decimal) -> ConsistencyBucket:
    """Convert a raw consistency multiplier to a client-safe enum bucket.

    Args:
        multiplier: The stored consistency_multiplier Decimal value.

    Returns:
        Client-safe ``ConsistencyBucket`` value.
    """
    f = float(multiplier)
    if f >= 1.2:
        return ConsistencyBucket.consistent
    if f >= 1.05:
        return ConsistencyBucket.regular
    return ConsistencyBucket.irregular


def _carbon_bucket_from_penalty(penalty: Decimal) -> CarbonBucket:
    """Map stored carbon_penalty to a client-safe bucket.

    The raw penalty value is NEVER returned; only the bucket label is exposed.

    Args:
        penalty: Stored carbon_penalty Decimal value.

    Returns:
        Client-safe ``CarbonBucket`` value.
    """
    p = float(penalty)
    if p >= 70.0:
        return CarbonBucket.high
    if p >= 40.0:
        return CarbonBucket.medium
    if p > 0.0:
        return CarbonBucket.low
    return CarbonBucket.none


def _toxicity_bucket_from_penalty(penalty: Decimal) -> ToxicityBucket:
    """Map stored toxicity_penalty to a client-safe bucket.

    The raw penalty value is NEVER returned; only the bucket label is exposed.

    Args:
        penalty: Stored toxicity_penalty Decimal value.

    Returns:
        Client-safe ``ToxicityBucket`` value.
    """
    p = float(penalty)
    if p >= 40.0:
        return ToxicityBucket.warning
    if p > 0.0:
        return ToxicityBucket.caution
    return ToxicityBucket.clean


# ── Existing schemas (kept for backward compatibility) ────────────────────────

class ScoreResponse(BaseModel):
    """Raw ORM-level score response (used by /users/me/score and leaderboard).

    ORM columns (total_score, score_level) are mapped via validation_alias
    so the API surface uses the spec names (final_score, level) while the
    DB schema stays unchanged.
    """

    id: uuid.UUID
    user_id: uuid.UUID
    final_score: Decimal = Field(validation_alias="total_score")
    social_impact: Decimal
    environmental: Decimal
    knowledge_innovation: Decimal
    economic_contribution: Decimal
    cultural_artistic: Decimal
    civic_political: Decimal
    level: str = Field(validation_alias="score_level")
    calculated_at: datetime

    model_config = {"from_attributes": True, "populate_by_name": True}


class ScoreSummary(BaseModel):
    """Minimal score summary embedded in public user profiles."""

    final_score: Decimal = Field(validation_alias="total_score")
    level: str = Field(validation_alias="score_level")
    rank: int | None = None

    model_config = {"from_attributes": True, "populate_by_name": True}


# ── New TASK-8 schemas ────────────────────────────────────────────────────────

class LevelInfo(BaseModel):
    """Human-readable level metadata."""

    name: str
    emoji: str
    range: list[int]


class ScorePublic(BaseModel):
    """Public score summary — no auth required.

    Response for GET /scores/{username}.
    """

    username: str
    final_score: float
    level: LevelInfo
    global_percentile: float | None = None
    calculated_at: datetime


class CategoryDetail(BaseModel):
    """Per-category score breakdown entry.

    All values are client-safe; no raw hidden-factor data.
    """

    score: float
    weight: float
    contribution: float


class HiddenAdjustments(BaseModel):
    """Client-safe hidden-factor bucket labels.

    Raw values (kg CO2, toxicity index, penalty amounts, multiplier floats)
    MUST NEVER appear here — only named bucket strings and booleans.
    """

    carbon_bucket: CarbonBucket
    toxicity_bucket: ToxicityBucket
    network_effect: NetworkEffect
    consistency: ConsistencyBucket
    equity_boost: bool


class BreakdownResponse(BaseModel):
    """Full authenticated score breakdown.

    Response for GET /scores/me/breakdown.
    """

    final_score: float
    level: LevelInfo
    categories: dict[str, CategoryDetail]
    hidden_adjustments: HiddenAdjustments


class RecalculateResponse(BaseModel):
    """Response for POST /scores/me/recalculate."""

    task_id: str
    status: str
