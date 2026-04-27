---
id: TASK-19
assignee: []
title: "Neo4j Graph Layer + Network Multiplier"
status: To Do
priority: medium
labels: ["epic003-mhs-scoring-engine", "sonnet", "developer"]
dependencies:
  - task-2
  - task-7
acceptance_criteria:
  - "Neo4j service starts in Docker Compose"
  - "`INSPIRED_BY` relationship created when user adds \"inspired by\" link"
  - "Network multiplier returns 1.0 for isolated user"
  - "Network multiplier returns > 1.0 for user with inspired followers"
  - "Capped at 1.5 even with large network"
  - "All graph mutations transactional (no partial writes)"
  - "Graph queries complete in < 200ms for typical depth-3 traversal"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-003 MHS Scoring Engine
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 35000
mhs_estimated_hours: 4
---

# TASK-019 — Neo4j Graph Layer + Network Multiplier

## Description
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

## Acceptance Criteria
- [ ] Neo4j service starts in Docker Compose
- [ ] `INSPIRED_BY` relationship created when user adds "inspired by" link
- [ ] Network multiplier returns 1.0 for isolated user
- [ ] Network multiplier returns > 1.0 for user with inspired followers
- [ ] Capped at 1.5 even with large network
- [ ] All graph mutations transactional (no partial writes)
- [ ] Graph queries complete in < 200ms for typical depth-3 traversal
