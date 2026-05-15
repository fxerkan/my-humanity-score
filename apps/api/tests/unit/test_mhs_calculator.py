"""Unit tests for MHSCalculator / compute_score — no I/O required."""

import random
import uuid
from decimal import Decimal

import pytest

from services.score_calculator import (
    MAX_SCORE,
    MIN_SCORE,
    MHSCalculator,
    ScoreInput,
    compute_score,
)

# ── Helpers ───────────────────────────────────────────────────────────────────

def _full_inp(**overrides: float) -> ScoreInput:
    """Return a ScoreInput with all categories at 500 (mid-range) + overrides."""
    base = {
        "social_impact": 500.0,
        "environmental": 500.0,
        "knowledge_innovation": 500.0,
        "economic_contribution": 500.0,
        "cultural_artistic": 500.0,
        "civic_political": 500.0,
    }
    base.update(overrides)
    return ScoreInput(**base)


# ── Zero score ────────────────────────────────────────────────────────────────

def test_zero_score_for_empty_input() -> None:
    """User with no activities has a final score of 0."""
    result = compute_score(ScoreInput())
    assert result.final_score == 0.0
    assert result.level == "awakening"


# ── All categories populated ──────────────────────────────────────────────────

def test_score_with_all_categories() -> None:
    """Score with all categories populated is > 0 and <= 1000."""
    result = compute_score(_full_inp())
    assert result.final_score > 0.0
    assert result.final_score <= MAX_SCORE
    for cat in result.category_scores:
        assert result.category_scores[cat] >= 0.0


# ── Carbon penalty thresholds ─────────────────────────────────────────────────

@pytest.mark.parametrize(
    "kg, no_penalty_score, has_penalty",
    [
        (0, True, False),
        (999, True, False),
        (1000, False, True),   # medium penalty applied
        (5000, False, True),   # high penalty applied
        (10_000, False, True), # max penalty applied
        (20_000, False, True), # capped at max
    ],
)
def test_carbon_penalty_reduces_score(kg: float, no_penalty_score: bool, has_penalty: bool) -> None:
    """Carbon footprint reduces the total score (verified via score delta, not raw penalty)."""
    baseline = compute_score(ScoreInput(social_impact=500.0))
    penalised = compute_score(ScoreInput(social_impact=500.0, carbon_kg_per_year=kg))
    if has_penalty:
        assert penalised.final_score < baseline.final_score
    else:
        assert penalised.final_score == baseline.final_score


# ── Toxicity penalty reduces score ───────────────────────────────────────────

@pytest.mark.parametrize(
    "toxicity, has_penalty",
    [
        (0.0, False),
        (0.49, False),
        (0.5, True),   # medium toxicity → penalty
        (0.85, True),  # high toxicity → max penalty
        (1.0, True),
    ],
)
def test_toxicity_penalty_reduces_score(toxicity: float, has_penalty: bool) -> None:
    """Toxicity index reduces the total score (verified via score delta, not raw penalty)."""
    baseline = compute_score(ScoreInput(social_impact=500.0))
    penalised = compute_score(ScoreInput(social_impact=500.0, toxicity_index=toxicity))
    if has_penalty:
        assert penalised.final_score < baseline.final_score
    else:
        assert penalised.final_score == baseline.final_score


# ── Network multiplier ────────────────────────────────────────────────────────

def test_network_multiplier_neutral() -> None:
    base = compute_score(_full_inp())
    with_mult = compute_score(_full_inp(network_multiplier=1.0))
    assert base.final_score == with_mult.final_score


def test_network_multiplier_capped_at_1_5() -> None:
    """A multiplier > 1.5 is clamped to 1.5."""
    at_cap = compute_score(_full_inp(network_multiplier=1.5))
    over_cap = compute_score(_full_inp(network_multiplier=99.0))
    assert at_cap.final_score == over_cap.final_score


# ── Score bounds (fuzz) ───────────────────────────────────────────────────────

def test_score_never_below_zero_or_above_1000() -> None:
    """Random inputs must always produce a score in [0, 1000]."""
    rng = random.Random(42)
    for _ in range(200):
        inp = ScoreInput(
            social_impact=rng.uniform(0, 2000),
            environmental=rng.uniform(0, 2000),
            knowledge_innovation=rng.uniform(0, 2000),
            economic_contribution=rng.uniform(0, 2000),
            cultural_artistic=rng.uniform(0, 2000),
            civic_political=rng.uniform(0, 2000),
            carbon_kg_per_year=rng.uniform(0, 50_000),
            toxicity_index=rng.uniform(0.0, 1.0),
            network_multiplier=rng.uniform(0.5, 5.0),
            consistency_multiplier=rng.uniform(0.5, 5.0),
            geo_equity_multiplier=rng.uniform(0.5, 5.0),
        )
        result = compute_score(inp)
        assert MIN_SCORE <= result.final_score <= MAX_SCORE, (
            f"Score {result.final_score} out of range for input {inp}"
        )


# ── Level assignment ──────────────────────────────────────────────────────────

@pytest.mark.parametrize(
    "total, expected_level",
    [
        (0.0, "awakening"),
        (50.0, "awakening"),
        (99.9, "awakening"),
        (100.0, "rising_star"),
        (249.9, "rising_star"),
        (250.0, "contributor"),
        (399.9, "contributor"),
        (400.0, "impact_maker"),
        (549.9, "impact_maker"),
        (550.0, "change_agent"),
        (699.9, "change_agent"),
        (700.0, "humanity_champion"),
        (849.9, "humanity_champion"),
        (850.0, "humanity_legend"),
        (1000.0, "humanity_legend"),
    ],
)
def test_score_levels(total: float, expected_level: str) -> None:
    """Each score range maps to the correct level string."""
    # Build a ScoreInput that produces approximately the target total
    # by back-calculating social_impact (weight 0.25, so 4× total needed)
    raw = total / 0.25
    inp = ScoreInput(social_impact=raw)
    result = compute_score(inp)
    assert result.level == expected_level, (
        f"Total={result.final_score:.1f} → level={result.level!r}, "
        f"expected={expected_level!r}"
    )


# ── MHSCalculator wrapper ─────────────────────────────────────────────────────

def test_mhs_calculator_compute_passthrough() -> None:
    """MHSCalculator.compute() delegates to compute_score correctly."""
    inp = _full_inp(social_impact=1000.0)
    via_calc = MHSCalculator.compute(inp)
    direct = compute_score(inp)
    assert via_calc.final_score == direct.final_score
    assert via_calc.level == direct.level


@pytest.mark.asyncio
async def test_mhs_calculator_calculate_returns_score_result() -> None:
    """MHSCalculator.calculate() returns a ScoreResult dataclass with AC-spec field names."""
    from unittest.mock import patch

    from services.score_calculator import ScoreResult

    calc = MHSCalculator()
    with patch(
        "services.network_multiplier.calculate_network_multiplier", return_value=1.0
    ):
        result = await calc.calculate(uuid.uuid4())
    assert isinstance(result, ScoreResult)
    # AC-required field names
    assert hasattr(result, "final_score")
    assert hasattr(result, "level")
    assert hasattr(result, "category_scores")
    assert hasattr(result, "carbon_bucket")
    assert hasattr(result, "toxicity_bucket")
    # Deprecated / forbidden field names must NOT be present
    assert not hasattr(result, "total_score")
    assert not hasattr(result, "score_level")
    assert not hasattr(result, "carbon_penalty")
    assert not hasattr(result, "toxicity_penalty")


@pytest.mark.asyncio
async def test_mhs_calculator_calculate_zero_score_for_stub() -> None:
    """MHSCalculator.calculate() returns 0.0 when no activities exist (stub)."""
    from unittest.mock import patch

    calc = MHSCalculator()
    with patch(
        "services.network_multiplier.calculate_network_multiplier", return_value=1.0
    ):
        result = await calc.calculate(uuid.uuid4())
    assert result.final_score == 0.0
    assert result.level == "awakening"


def test_mhs_calculator_score_from_decimal() -> None:
    """MHSCalculator.score_from_decimal() converts Decimal to float."""
    value = Decimal("342.75")
    assert MHSCalculator.score_from_decimal(value) == pytest.approx(342.75)
    assert isinstance(MHSCalculator.score_from_decimal(value), float)


def test_mhs_calculator_score_from_decimal_zero() -> None:
    """MHSCalculator.score_from_decimal() handles zero Decimal correctly."""
    assert MHSCalculator.score_from_decimal(Decimal("0")) == 0.0


# ── Hidden factors never exposed raw ──────────────────────────────────────────

def test_score_result_contains_buckets_not_raw_values() -> None:
    """ScoreResult exposes only bucket strings — no raw hidden factor values."""
    inp = ScoreInput(carbon_kg_per_year=12_000, toxicity_index=0.9)
    result = compute_score(inp)
    # Buckets must be string labels
    assert isinstance(result.carbon_bucket, str)
    assert isinstance(result.toxicity_bucket, str)
    assert result.carbon_bucket in {"low", "medium", "high"}
    assert result.toxicity_bucket in {"low", "medium", "high"}
    # Raw hidden-factor numeric fields must not exist on ScoreResult
    for forbidden in ("carbon_penalty", "toxicity_penalty", "carbon_kg_per_year", "toxicity_index"):
        assert not hasattr(result, forbidden), f"ScoreResult must not expose raw field: {forbidden}"


# ── Max score boundary ────────────────────────────────────────────────────────

def test_max_score_clamped_at_1000() -> None:
    """Even with extreme inputs and best multipliers, score never exceeds 1000."""
    inp = ScoreInput(
        social_impact=10_000.0,
        environmental=10_000.0,
        knowledge_innovation=10_000.0,
        economic_contribution=10_000.0,
        cultural_artistic=10_000.0,
        civic_political=10_000.0,
        network_multiplier=1.5,
        consistency_multiplier=1.3,
        geo_equity_multiplier=1.3,
    )
    result = compute_score(inp)
    assert result.final_score == MAX_SCORE


# ── Carbon bucket boundaries ──────────────────────────────────────────────────

@pytest.mark.parametrize(
    "kg, expected_bucket",
    [
        (0, "low"),
        (999, "low"),
        (1000, "medium"),
        (4999, "medium"),
        (5000, "high"),
        (10_000, "high"),
    ],
)
def test_carbon_bucket_values(kg: float, expected_bucket: str) -> None:
    """Carbon bucket labels map correctly to kg thresholds."""
    inp = ScoreInput(carbon_kg_per_year=kg)
    result = compute_score(inp)
    assert result.carbon_bucket == expected_bucket
    # Carbon penalty must NOT be a raw field on ScoreResult
    assert not hasattr(result, "carbon_penalty")


# ── Toxicity bucket boundaries ────────────────────────────────────────────────

@pytest.mark.parametrize(
    "toxicity, expected_bucket",
    [
        (0.0, "low"),
        (0.49, "low"),
        (0.5, "medium"),
        (0.84, "medium"),
        (0.85, "high"),
        (1.0, "high"),
    ],
)
def test_toxicity_bucket_values(toxicity: float, expected_bucket: str) -> None:
    """Toxicity bucket labels map correctly to index thresholds."""
    inp = ScoreInput(toxicity_index=toxicity)
    result = compute_score(inp)
    assert result.toxicity_bucket == expected_bucket
