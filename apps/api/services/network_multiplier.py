"""Network multiplier: hidden factor derived from Neo4j inspiration graph.

The multiplier is computed exclusively via Cypher graph queries.
It MUST NOT be exposed as a raw float in any API response — only
client-safe bucket labels (``NetworkEffect``) are returned.

Calculation::

    multiplier = 1.0 + (inspired_count * 0.05)
    multiplier = clamp(multiplier, 1.0, 1.5)

where *inspired_count* is the number of distinct users who declared
the target user as their inspiration, traversed up to depth 3.
"""

from __future__ import annotations

import logging

from graph.client import neo4j_session
from graph.queries import COUNT_INSPIRED_USERS, run_query

logger = logging.getLogger(__name__)

# ── Constants ────────────────────────────────────────────────────────────────

_MULTIPLIER_PER_INSPIRED: float = 0.05
_MAX_NETWORK_MULTIPLIER: float = 1.5
_MIN_NETWORK_MULTIPLIER: float = 1.0


async def calculate_network_multiplier(user_id: str) -> float:
    """Calculate the network multiplier for a user via Neo4j.

    Queries the inspiration graph for users who cited *user_id* as
    inspiration (traversed up to depth 3).  The multiplier is computed as::

        result = 1.0 + (inspired_count * 0.05)
        result = min(max(result, 1.0), 1.5)

    If Neo4j is unavailable the function logs a warning and returns 1.0
    (neutral — no network benefit, no penalty).

    Args:
        user_id: UUID string of the user.

    Returns:
        Float multiplier in [1.0, 1.5].
    """
    try:
        async with neo4j_session() as session:
            records = await run_query(session, COUNT_INSPIRED_USERS, user_id=user_id)
            inspired_count = records[0]["inspired_count"] if records else 0
    except Exception as exc:
        logger.warning(
            "Neo4j query failed for user_id=%s — returning neutral multiplier: %s",
            user_id,
            exc,
        )
        return _MIN_NETWORK_MULTIPLIER

    multiplier = _MIN_NETWORK_MULTIPLIER + (inspired_count * _MULTIPLIER_PER_INSPIRED)
    return max(_MIN_NETWORK_MULTIPLIER, min(multiplier, _MAX_NETWORK_MULTIPLIER))


async def add_inspiration(follower_id: str, inspiration_id: str) -> None:
    """Record that *follower_id* was inspired by *inspiration_id*.

    Args:
        follower_id: UUID string of the user who declares inspiration.
        inspiration_id: UUID string of the user who inspired them.

    Raises:
        ValueError: If follower attempts to self-inspire.
    """
    from graph.client import neo4j_session
    from graph.queries import CREATE_INSPIRED_BY, MERGE_USER, run_query

    if follower_id == inspiration_id:
        raise ValueError("Cannot be inspired by yourself")

    async with neo4j_session() as session:
        # Ensure both user nodes exist in the graph
        await run_query(session, MERGE_USER, user_id=follower_id, username="")
        await run_query(session, MERGE_USER, user_id=inspiration_id, username="")
        # Create the inspiration edge
        await run_query(
            session,
            CREATE_INSPIRED_BY,
            follower_id=follower_id,
            inspiration_id=inspiration_id,
        )


async def remove_inspiration(follower_id: str, inspiration_id: str) -> bool:
    """Remove an inspiration relationship.

    Returns True if a relationship was deleted, False otherwise.
    """
    from graph.client import neo4j_session
    from graph.queries import REMOVE_INSPIRED_BY, run_query

    async with neo4j_session() as session:
        records = await run_query(
            session,
            REMOVE_INSPIRED_BY,
            follower_id=follower_id,
            inspiration_id=inspiration_id,
        )
        return records[0]["deleted_count"] > 0 if records else False


async def setup_schema() -> None:
    """Create Neo4j constraints and indexes for the graph schema.

    Safe to call multiple times — uses IF NOT EXISTS clauses.
    """
    from graph.client import neo4j_session
    from graph.queries import (
        CREATE_ACTIVITY_CONSTRAINT,
        CREATE_CONSTRAINTS,
        CREATE_INSPIRED_BY_INDEX,
        CREATE_ORG_CONSTRAINT,
        run_query,
    )

    async with neo4j_session() as session:
        await run_query(session, CREATE_CONSTRAINTS)
        await run_query(session, CREATE_ACTIVITY_CONSTRAINT)
        await run_query(session, CREATE_ORG_CONSTRAINT)
        await run_query(session, CREATE_INSPIRED_BY_INDEX)
        logger.info("Neo4j graph schema initialised")
