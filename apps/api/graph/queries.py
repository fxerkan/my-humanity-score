"""Cypher query functions — NO inline strings in application code.

All Cypher statements are defined here as module-level constants.
Parameterised queries accept ``**kwargs`` that are passed as Neo4j
query parameters (auto‑escaped by the driver).
"""

from __future__ import annotations

from typing import Any

# ── Schema setup ─────────────────────────────────────────────────────────────

CREATE_CONSTRAINTS = """
CREATE CONSTRAINT unique_user_id IF NOT EXISTS
FOR (u:User) REQUIRE u.id IS UNIQUE
"""

CREATE_ACTIVITY_CONSTRAINT = """
CREATE CONSTRAINT unique_activity_id IF NOT EXISTS
FOR (a:Activity) REQUIRE a.id IS UNIQUE
"""

CREATE_ORG_CONSTRAINT = """
CREATE CONSTRAINT unique_org_id IF NOT EXISTS
FOR (o:Organization) REQUIRE o.id IS UNIQUE
"""

CREATE_INSPIRED_BY_INDEX = """
CREATE INDEX inspired_by_index IF NOT EXISTS
FOR ()-[r:INSPIRED_BY]-() ON (r.created_at)
"""

# ── Node creation / merge ────────────────────────────────────────────────────

MERGE_USER = """
MERGE (u:User {id: $user_id})
  ON CREATE SET u.username = $username
  ON MATCH  SET u.username = $username
RETURN u
"""

MERGE_ACTIVITY = """
MERGE (a:Activity {id: $activity_id})
  ON CREATE SET a.type = $type, a.impact_score = $impact_score
  ON MATCH  SET a.type = $type, a.impact_score = $impact_score
RETURN a
"""

# ── Relationships ────────────────────────────────────────────────────────────

CREATE_INSPIRED_BY = """
MATCH (follower:User {id: $follower_id})
MATCH (inspiration:User {id: $inspiration_id})
MERGE (follower)-[r:INSPIRED_BY]->(inspiration)
  ON CREATE SET r.created_at = datetime()
RETURN r
"""

REMOVE_INSPIRED_BY = """
MATCH (follower:User {id: $follower_id})-[r:INSPIRED_BY]->(inspiration:User {id: $inspiration_id})
DELETE r
RETURN count(r) AS deleted_count
"""

CREATE_PERFORMED = """
MATCH (u:User {id: $user_id})
MATCH (a:Activity {id: $activity_id})
MERGE (u)-[:PERFORMED]->(a)
"""

CREATE_PART_OF = """
MATCH (a:Activity {id: $activity_id})
MATCH (o:Organization {id: $org_id})
MERGE (a)-[:PART_OF]->(o)
"""

CREATE_FOLLOWS = """
MATCH (follower:User {id: $follower_id})
MATCH (followee:User {id: $followee_id})
MERGE (follower)-[:FOLLOWS]->(followee)
"""

REMOVE_FOLLOWS = """
MATCH (follower:User {id: $follower_id})-[r:FOLLOWS]->(followee:User {id: $followee_id})
DELETE r
RETURN count(r) AS deleted_count
"""

# ── Queries ──────────────────────────────────────────────────────────────────

COUNT_INSPIRED_USERS = """
MATCH (u:User {id: $user_id})<-[:INSPIRED_BY*1..3]-(inspired:User)
RETURN count(DISTINCT inspired) AS inspired_count
"""

GET_INSPIRATION_CHAIN = """
MATCH path = (u:User {id: $user_id})<-[:INSPIRED_BY*1..$depth]-(inspired:User)
RETURN inspired.id AS user_id, length(path) AS depth
ORDER BY depth
"""

GET_FOLLOWERS = """
MATCH (u:User {id: $user_id})<-[:FOLLOWS]-(follower:User)
RETURN follower.id AS user_id, follower.username AS username
LIMIT $limit
"""

GET_FOLLOWING = """
MATCH (u:User {id: $user_id})-[:FOLLOWS]->(followed:User)
RETURN followed.id AS user_id, followed.username AS username
LIMIT $limit
"""

COUNT_ACTIVITIES_BY_INSPIRED = """
MATCH (u:User {id: $user_id})<-[:INSPIRED_BY*1..3]-(inspired:User)-[:PERFORMED]->(a:Activity)
RETURN count(DISTINCT a) AS activity_count
"""

# ── Helper to run a parameterised query ──────────────────────────────────────


async def run_query(
    session: Any,
    query: str,
    **params: Any,
) -> list[dict[str, Any]]:
    """Execute a parameterised Cypher query and return records as dicts.

    Args:
        session: An active Neo4j async session.
        query: Cypher query string (use module constants).
        **params: Named query parameters.

    Returns:
        List of record dicts.
    """
    result = await session.run(query, **params)
    records = await result.data()
    return records  # type: ignore[no-any-return]
