---
id: TASK-19
title: Neo4j Graph Layer + Network Multiplier
status: In Progress
assignee:
  - '@agent-k'
created_date: '2026-04-27 13:41'
updated_date: '2026-05-14 20:47'
labels:
  - epic003-mhs-scoring-engine
  - sonnet
  - developer
dependencies:
  - task-2
  - task-7
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement the Neo4j graph layer for tracking inspiration chains and
computing the network multiplier hidden factor.

## Graph schema
```cypher
(:User {id, username, mhs_score})
(:Activity {id, type, impact_score})
(:Organization {id, name, type})

(:User)-[:INSPIRED_BY]->(:User)        // direct inspiration
(:User)-[:PERFORMED]->(:Activity)
(:Activity)-[:PART_OF]->(:Organization)
(:User)-[:FOLLOWS]->(:User)
```

## Network multiplier calculation
```python
def network_multiplier(user_id: str) -> float:
    # Traverse inspiration chain up to depth 3
    # Count users who cited this user as inspiration
    # Count activities by inspired users
    # multiplier = 1.0 + (inspired_count * 0.05), capped at 1.5
    # Min: 1.0 (no network effect), Max: 1.5
```

## Cypher query (network multiplier)
```cypher
MATCH (u:User {id: $user_id})<-[:INSPIRED_BY*1..3]-(inspired:User)
RETURN count(DISTINCT inspired) AS inspired_count
```

## Python driver
- Library: `neo4j` (official Python driver)
- Connection pool managed by FastAPI lifespan
- All Cypher queries in `apps/api/graph/queries.py` (no inline strings)

## Sync strategy
- User follows → written to Neo4j immediately
- Activity completed → Neo4j updated within 30 seconds (Celery)
- Network multiplier recalculated as part of score recalculation
<!-- SECTION:DESCRIPTION:END -->

# TASK-019 — Neo4j Graph Layer + Network Multiplier

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Neo4j service starts in Docker Compose
- [x] #2 `INSPIRED_BY` relationship created when user adds "inspired by" link
- [x] #3 Network multiplier returns 1.0 for isolated user
- [x] #4 Network multiplier returns > 1.0 for user with inspired followers
- [x] #5 Capped at 1.5 even with large network
- [x] #6 All graph mutations transactional (no partial writes)
- [x] #7 Graph queries complete in < 200ms for typical depth-3 traversal
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add neo4j driver to requirements.txt
2. Add NEO4J_URI/NEO4J_USER/NEO4J_PASSWORD to config.py
3. Create apps/api/graph/client.py — Neo4j driver with FastAPI lifespan
4. Create apps/api/graph/queries.py — all Cypher queries
5. Create apps/api/services/network_multiplier.py — business logic
6. Create POST /users/{username}/inspire endpoint to create INSPIRED_BY edge
7. Wire multiplier into score recalculation flow
8. Run tests and verify
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Set up Neo4j graph database layer and implemented the network multiplier hidden scoring factor.

## Changes

### Graph layer (apps/api/graph/)
- **client.py**: Async Neo4j driver with connection pool, FastAPI lifespan integration, connectivity verification, graceful degradation when Neo4j is unavailable
- **queries.py**: 18 parameterised Cypher queries (MERGE user/activity nodes, CREATE INSPIRED_BY/FOLLOWS/PERFORMED/PART_OF relationships, COUNT_INSPIRED_USERS for multiplier, schema constraints/indexes)

### Network multiplier (apps/api/services/network_multiplier.py)
- Multiplier = 1.0 + (inspired_count * 0.05), capped at [1.0, 1.5]
- Traverses INSPIRED_BY chain up to depth 3
- Returns 1.0 (neutral) when Neo4j is unavailable — no hard dependency

### API endpoints
- POST /users/me/inspire — creates INSPIRED_BY edge in Neo4j
- DELETE /users/me/inspire/{username} — removes inspiration relationship

### Score integration
- MHSCalculator.calculate() updated to async, queries Neo4j for network multiplier
- Celery recalculate_score task uses asyncio.run() for the async calculator

### Infrastructure
- docker-compose.yml: NEO4J_URI/USER/PASSWORD env vars added to api + worker services
- Neo4j service already configured with profiles [graph, full] (--profile full up)

### Tests
- 14 new unit tests (isolated user=1.0, single inspired=1.05, capped at 1.5, Neo4j unavailable fallback, add/remove inspiration, schema setup, calculator integration)
- All 114 tests passing
<!-- SECTION:FINAL_SUMMARY:END -->
