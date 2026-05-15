"""Unit tests for the network multiplier service.

Neo4j is mocked — NO real database connection required.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.network_multiplier import (
    _MAX_NETWORK_MULTIPLIER,
    _MIN_NETWORK_MULTIPLIER,
    add_inspiration,
    calculate_network_multiplier,
    remove_inspiration,
    setup_schema,
)


def _mock_session(data: list[dict]) -> MagicMock:
    """Return an async mock session that yields the given data."""
    mock = MagicMock()
    mock_result = AsyncMock()
    mock_result.data = AsyncMock(return_value=data)
    mock.run = AsyncMock(return_value=mock_result)
    return mock


def _patch_neo4j_session(mock_session: MagicMock):
    """Patch neo4j_session in both ``graph.client`` and
    ``services.network_multiplier`` to yield *mock_session*.

    Returns a contextlib.ExitStack that applies all patches and undoes
    them on exit.  Use as::

        with _patch_neo4j_session(session):
            ...
    """
    import contextlib

    class _FakeSession:
        """Callable → async context manager that yields *mock_session*."""

        def __init__(self, session: MagicMock):
            self._session = session

        def __call__(self):
            return self

        async def __aenter__(self):
            return self._session

        async def __aexit__(self, *args):
            pass

    mock_driver = MagicMock()
    fake_session = _FakeSession(mock_session)
    stack = contextlib.ExitStack()

    # Patch module-level import in services.network_multiplier
    stack.enter_context(
        patch("services.network_multiplier.neo4j_session", new=fake_session),
    )
    # Patch graph.client for lazy imports in add_inspiration etc.
    stack.enter_context(
        patch.multiple(
            "graph.client",
            neo4j_session=fake_session,
            get_neo4j_driver=AsyncMock(return_value=mock_driver),
        ),
    )
    return stack


# ── calculate_network_multiplier ─────────────────────────────────────────────


@pytest.mark.asyncio
async def test_network_multiplier_isolated_user_returns_1_0() -> None:
    """An isolated user with no inspired followers → 1.0 multiplier."""
    session = _mock_session([{"inspired_count": 0}])
    with _patch_neo4j_session(session):
        result = await calculate_network_multiplier("user-1")
    assert result == 1.0


@pytest.mark.asyncio
async def test_network_multiplier_single_inspired() -> None:
    """One inspired follower → multiplier = 1.0 + 1 * 0.05 = 1.05."""
    session = _mock_session([{"inspired_count": 1}])
    with _patch_neo4j_session(session):
        result = await calculate_network_multiplier("user-2")
    assert result == 1.05


@pytest.mark.asyncio
async def test_network_multiplier_many_inspired() -> None:
    """Multiple inspired followers = 1.0 + N * 0.05."""
    session = _mock_session([{"inspired_count": 6}])
    with _patch_neo4j_session(session):
        result = await calculate_network_multiplier("user-3")
    assert result == 1.0 + 6 * 0.05  # 1.3


@pytest.mark.asyncio
async def test_network_multiplier_capped_at_1_5() -> None:
    """More than 10 inspired → capped at 1.5."""
    session = _mock_session([{"inspired_count": 50}])
    with _patch_neo4j_session(session):
        result = await calculate_network_multiplier("user-4")
    assert result == _MAX_NETWORK_MULTIPLIER


@pytest.mark.asyncio
async def test_network_multiplier_exactly_at_cap() -> None:
    """10 inspired = 1.0 + 10 * 0.05 = 1.5 exactly."""
    session = _mock_session([{"inspired_count": 10}])
    with _patch_neo4j_session(session):
        result = await calculate_network_multiplier("user-9")
    assert result == 1.5


@pytest.mark.asyncio
async def test_network_multiplier_max_edge() -> None:
    """9 inspired = 1.45 — just under the cap."""
    session = _mock_session([{"inspired_count": 9}])
    with _patch_neo4j_session(session):
        result = await calculate_network_multiplier("user-5")
    assert result == 1.45


@pytest.mark.asyncio
async def test_network_multiplier_empty_records() -> None:
    """No records returned from Neo4j → 1.0 (defensive)."""
    session = _mock_session([])
    with _patch_neo4j_session(session):
        result = await calculate_network_multiplier("user-6")
    assert result == _MIN_NETWORK_MULTIPLIER


@pytest.mark.asyncio
async def test_network_multiplier_neo4j_unavailable_returns_1_0() -> None:
    """When Neo4j is unavailable, return neutral 1.0."""
    with patch(
        "services.network_multiplier.neo4j_session",
        side_effect=OSError("Connection refused"),
    ):
        result = await calculate_network_multiplier("user-7")
    assert result == _MIN_NETWORK_MULTIPLIER


# ── add_inspiration ──────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_add_inspiration_success() -> None:
    """Creating an INSPIRED_BY edge succeeds."""
    session = _mock_session([])
    with _patch_neo4j_session(session):
        await add_inspiration("follower-1", "hero-1")
        assert session.run.call_count == 3


@pytest.mark.asyncio
async def test_add_inspiration_self_reference_raises() -> None:
    """Self-inspiration is forbidden via ValueError → 400."""
    with pytest.raises(ValueError, match="yourself"):
        await add_inspiration("same-id", "same-id")


# ── remove_inspiration ───────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_remove_inspiration_success() -> None:
    """Removing an existing edge returns True."""
    session = _mock_session([{"deleted_count": 1}])
    with _patch_neo4j_session(session):
        result = await remove_inspiration("follower-1", "hero-1")
        assert result is True


@pytest.mark.asyncio
async def test_remove_inspiration_not_found() -> None:
    """Removing a non-existent edge returns False."""
    session = _mock_session([{"deleted_count": 0}])
    with _patch_neo4j_session(session):
        result = await remove_inspiration("follower-1", "no-one")
        assert result is False


# ── setup_schema ─────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_setup_schema_runs_all_statements() -> None:
    """Schema setup executes all 4 constraint/index statements."""
    session = _mock_session([])
    with _patch_neo4j_session(session):
        await setup_schema()
        assert session.run.call_count == 4


# ── Integration with score calculator ────────────────────────────────────────


@pytest.mark.asyncio
async def test_calculator_uses_network_multiplier() -> None:
    """MHSCalculator.calculate() queries Neo4j for the network multiplier."""
    from services.score_calculator import MHSCalculator, ScoreInput, compute_score

    calc = MHSCalculator()

    # Neutral multiplier (1.0) — score unchanged by network
    with patch(
        "services.network_multiplier.calculate_network_multiplier",
        return_value=1.0,
    ):
        result_neutral = await calc.calculate("user-1")
        assert 0.0 <= result_neutral.final_score <= 1000.0

    # Max multiplier (1.5)
    with patch(
        "services.network_multiplier.calculate_network_multiplier",
        return_value=_MAX_NETWORK_MULTIPLIER,
    ):
        result_max = await calc.calculate("user-2")
        assert 0.0 <= result_max.final_score <= 1000.0

    # Pure function: verify multiplier > 1.0 increases score
    result_1 = compute_score(ScoreInput(social_impact=500.0, network_multiplier=1.0))
    result_2 = compute_score(ScoreInput(social_impact=500.0, network_multiplier=1.5))
    assert result_2.final_score > result_1.final_score
