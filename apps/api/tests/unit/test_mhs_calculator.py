"""Unit tests for MHSCalculator / compute_score — no I/O required."""

import random

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
    """User with no activities has a total score of 0."""
    result = compute_score(ScoreInput())
    assert result.total_score == 0.0
    assert result.score_level == "awakening"


# ── All categories populated ──────────────────────────────────────────────────

def test_score_with_all_categories() -> None:
    """Score with all categories populated is > 0 and <= 1000."""
    result = compute_score(_full_inp())
    assert result.total_score > 0.0
    assert result.total_score <= MAX_SCORE
    for cat in result.category_totals:
        assert result.category_totals[cat] >= 0.0


# ── Carbon penalty thresholds ─────────────────────────────────────────────────

@pytest.mark.parametrize(
    "kg, expected_penalty",
    [
        (0, 0.0),
        (999, 0.0),
        (1000, 20.0),
        (4999, 20.0),
        (5000, 60.0),
        (9999, 60.0),
        (10_000, 100.0),
        (20_000, 100.0),  # capped at 100
    ],
)
def test_carbon_penalty_thresholds(kg: float, expected_penalty: float) -> None:
    inp = ScoreInput(carbon_kg_per_year=kg)
    result = compute_score(inp)
    assert result.carbon_penalty == expected_penalty


# ── Toxicity penalty thresholds ───────────────────────────────────────────────

@pytest.mark.parametrize(
    "toxicity, expected_penalty",
    [
        (0.0, 0.0),
        (0.49, 0.0),
        (0.5, 40.0),
        (0.84, 40.0),
        (0.85, 80.0),
        (1.0, 80.0),  # capped at 80
    ],
)
def test_toxicity_penalty_thresholds(toxicity: float, expected_penalty: float) -> None:
    inp = ScoreInput(toxicity_index=toxicity)
    result = compute_score(inp)
    assert result.toxicity_penalty == expected_penalty


# ── Network multiplier ────────────────────────────────────────────────────────

def test_network_multiplier_neutral() -> None:
    base = compute_score(_full_inp())
    with_mult = compute_score(_full_inp(network_multiplier=1.0))
    assert base.total_score == with_mult.total_score


def test_network_multiplier_capped_at_1_5() -> None:
    """A multiplier > 1.5 is clamped to 1.5."""
    at_cap = compute_score(_full_inp(network_multiplier=1.5))
    over_cap = compute_score(_full_inp(network_multiplier=99.0))
    assert at_cap.total_score == over_cap.total_score


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
        assert MIN_SCORE <= result.total_score <= MAX_SCORE, (
            f"Score {result.total_score} out of range for input {inp}"
        )


# ── Level assignment ──────────────────────────────────────────────────────────

@pytest.mark.parametrize(
    "total, expected_level",
    [
        (0.0, "awakening"),
        (50.0, "awakening"),
        (100.0, "rising_star"),
        (199.9, "rising_star"),
        (200.0, "contributor"),
        (350.0, "impact_maker"),
        (500.0, "change_agent"),
        (650.0, "humanity_champion"),
        (800.0, "humanity_legend"),
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
    assert result.score_level == expected_level, (
        f"Total={result.total_score:.1f} → level={result.score_level!r}, "
        f"expected={expected_level!r}"
    )


# ── MHSCalculator wrapper ─────────────────────────────────────────────────────

def test_mhs_calculator_compute_passthrough() -> None:
    """MHSCalculator.compute() delegates to compute_score correctly."""
    inp = _full_inp(social_impact=1000.0)
    via_calc = MHSCalculator.compute(inp)
    direct = compute_score(inp)
    assert via_calc.total_score == direct.total_score
    assert via_calc.score_level == direct.score_level
