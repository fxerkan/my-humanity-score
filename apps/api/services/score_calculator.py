"""MHS Score Calculator — pure Python, no I/O dependencies.

All scoring logic operates on plain dicts so it can be unit-tested
without a database.  The MHSCalculator.calculate() method wires it
to the ORM for production use.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any

# ── Category weights ────────────────────────────────────────────────────────
CATEGORY_WEIGHTS: dict[str, float] = {
    "social_impact": 0.25,
    "environmental": 0.20,
    "knowledge_innovation": 0.20,
    "economic_contribution": 0.15,
    "cultural_artistic": 0.10,
    "civic_political": 0.10,
}

MAX_SCORE: float = 1000.0
MIN_SCORE: float = 0.0

# ── Carbon penalty thresholds (kg CO2/year) ─────────────────────────────────
_CARBON_THRESHOLDS: list[tuple[float, float]] = [
    (10_000, 100.0),
    (5_000, 60.0),
    (1_000, 20.0),
    (0, 0.0),
]
MAX_CARBON_PENALTY: float = 100.0

# ── Toxicity penalty thresholds (0.0 – 1.0) ─────────────────────────────────
_TOXICITY_THRESHOLDS: list[tuple[float, float]] = [
    (0.85, 80.0),
    (0.5, 40.0),
    (0.0, 0.0),
]
MAX_TOXICITY_PENALTY: float = 80.0

# ── Score level ranges ───────────────────────────────────────────────────────
SCORE_LEVELS: list[tuple[float, str]] = [
    (800.0, "humanity_legend"),
    (650.0, "humanity_champion"),
    (500.0, "change_agent"),
    (350.0, "impact_maker"),
    (200.0, "contributor"),
    (100.0, "rising_star"),
    (0.0, "awakening"),
]

# ── Multiplier caps ──────────────────────────────────────────────────────────
MAX_NETWORK_MULTIPLIER: float = 1.5
MAX_CONSISTENCY_MULTIPLIER: float = 1.3
MAX_GEO_EQUITY_MULTIPLIER: float = 1.3


@dataclass
class ScoreInput:
    """Flat representation of all scoring inputs.

    Category scores are pre-weighted raw points (0–max_per_category).
    Multipliers default to 1.0 (neutral).
    """

    social_impact: float = 0.0
    environmental: float = 0.0
    knowledge_innovation: float = 0.0
    economic_contribution: float = 0.0
    cultural_artistic: float = 0.0
    civic_political: float = 0.0

    # Hidden adjustment factors — never exposed raw to clients
    carbon_kg_per_year: float = 0.0
    toxicity_index: float = 0.0  # 0.0–1.0
    network_multiplier: float = 1.0
    consistency_multiplier: float = 1.0
    geo_equity_multiplier: float = 1.0

    # Metadata
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class ScoreResult:
    """Computed MHS score and breakdown."""

    total_score: float
    score_level: str
    category_totals: dict[str, float]
    carbon_penalty: float
    toxicity_penalty: float
    # Client-safe buckets (never raw values)
    carbon_bucket: str
    toxicity_bucket: str


def compute_score(inp: ScoreInput) -> ScoreResult:
    """Pure function: compute MHS score from a ScoreInput.

    Args:
        inp: All scoring inputs (categories + adjustment factors).

    Returns:
        ScoreResult with total, level, and per-category breakdown.
    """
    # 1. Weighted category sum (each raw value already in 0–category_max range)
    category_totals: dict[str, float] = {
        cat: getattr(inp, cat) * weight
        for cat, weight in CATEGORY_WEIGHTS.items()
    }
    base_score = sum(category_totals.values())

    # 2. Apply multipliers (cap each)
    net_mult = min(inp.network_multiplier, MAX_NETWORK_MULTIPLIER)
    con_mult = min(inp.consistency_multiplier, MAX_CONSISTENCY_MULTIPLIER)
    geo_mult = min(inp.geo_equity_multiplier, MAX_GEO_EQUITY_MULTIPLIER)
    adjusted = base_score * net_mult * con_mult * geo_mult

    # 3. Apply penalties
    carbon_penalty = _carbon_penalty(inp.carbon_kg_per_year)
    toxicity_penalty = _toxicity_penalty(inp.toxicity_index)
    penalised = adjusted - carbon_penalty - toxicity_penalty

    # 4. Clamp to [0, 1000]
    total = max(MIN_SCORE, min(MAX_SCORE, penalised))

    return ScoreResult(
        total_score=round(total, 2),
        score_level=_score_level(total),
        category_totals={k: round(v, 2) for k, v in category_totals.items()},
        carbon_penalty=round(carbon_penalty, 2),
        toxicity_penalty=round(toxicity_penalty, 2),
        carbon_bucket=_carbon_bucket(inp.carbon_kg_per_year),
        toxicity_bucket=_toxicity_bucket(inp.toxicity_index),
    )


def _carbon_penalty(kg_per_year: float) -> float:
    """Map annual carbon footprint to a score penalty (0–100).

    Args:
        kg_per_year: Annual CO2 in kilograms.

    Returns:
        Penalty value between 0 and MAX_CARBON_PENALTY.
    """
    for threshold, penalty in _CARBON_THRESHOLDS:
        if kg_per_year >= threshold:
            return min(penalty, MAX_CARBON_PENALTY)
    return 0.0


def _toxicity_penalty(toxicity_index: float) -> float:
    """Map toxicity index (0.0–1.0) to a score penalty (0–80).

    Args:
        toxicity_index: Normalised toxicity score from the NLP classifier.

    Returns:
        Penalty value between 0 and MAX_TOXICITY_PENALTY.
    """
    for threshold, penalty in _TOXICITY_THRESHOLDS:
        if toxicity_index >= threshold:
            return min(penalty, MAX_TOXICITY_PENALTY)
    return 0.0


def _score_level(total: float) -> str:
    """Map a total score to a named level.

    Args:
        total: Final MHS score (0–1000).

    Returns:
        Level name string.
    """
    for min_score, level in SCORE_LEVELS:
        if total >= min_score:
            return level
    return "awakening"


def _carbon_bucket(kg_per_year: float) -> str:
    """Return client-safe carbon bucket (never raw kg value).

    Args:
        kg_per_year: Annual CO2 in kilograms.

    Returns:
        Bucket string: "low" | "medium" | "high".
    """
    if kg_per_year >= 5000:
        return "high"
    if kg_per_year >= 1000:
        return "medium"
    return "low"


def _toxicity_bucket(toxicity_index: float) -> str:
    """Return client-safe toxicity bucket (never raw index value).

    Args:
        toxicity_index: Normalised toxicity score 0.0–1.0.

    Returns:
        Bucket string: "low" | "medium" | "high".
    """
    if toxicity_index >= 0.85:
        return "high"
    if toxicity_index >= 0.5:
        return "medium"
    return "low"


class MHSCalculator:
    """Thin ORM wrapper around the pure compute_score() function.

    Fetches activity data from the database, builds a ScoreInput,
    calls compute_score(), and persists the result.
    """

    def calculate(self, user_id: uuid.UUID) -> dict[str, object]:
        """Calculate and persist the MHS score for a user.

        This is a synchronous stub — real aggregation queries implemented
        when activities API (TASK-010) and verification pipeline are complete.

        Args:
            user_id: UUID of the user to score.

        Returns:
            Dict with user_id and computed score fields.
        """
        # Stub input — real query aggregation in TASK-010
        inp = ScoreInput()
        result = compute_score(inp)
        return {
            "user_id": str(user_id),
            "total_score": result.total_score,
            "score_level": result.score_level,
            "category_totals": result.category_totals,
            "carbon_penalty": result.carbon_penalty,
            "toxicity_penalty": result.toxicity_penalty,
            "carbon_bucket": result.carbon_bucket,
            "toxicity_bucket": result.toxicity_bucket,
        }

    @staticmethod
    def compute(inp: ScoreInput) -> ScoreResult:
        """Public access to the pure compute function.

        Args:
            inp: ScoreInput dataclass.

        Returns:
            ScoreResult dataclass.
        """
        return compute_score(inp)

    @staticmethod
    def score_from_decimal(score: Decimal) -> float:
        """Convert a Decimal score to float for JSON serialisation.

        Args:
            score: Decimal score value.

        Returns:
            Float representation.
        """
        return float(score)
