# EPIC-003 — MHS Scoring Engine

## Status: `blocked` (needs EPIC-001)
## Priority: P1 (Sprint 2)

## Goal
Implement the core MHS score calculator with 6 weighted categories and
5 hidden adjustment factors, exposed via API.

## Scope
- MHSCalculator Python class (from concept/MHS_KB_02_Technical.md)
- 6 category weights: Social Impact 25%, Environmental 20%, Knowledge 20%,
  Economic 15%, Cultural 10%, Civic 10%
- Hidden factors: carbon penalty (0 to -100), toxicity penalty (0 to -80),
  network multiplier (1.0-1.5x), consistency multiplier, geographic equity (1.0-1.3x)
- Score clamped to 0-1000
- 7 level badges assigned automatically
- API endpoints for score + category breakdown
- Leaderboard (global, regional, category)
- Neo4j graph layer for network multiplier

## Tasks
- TASK-007: MHS score calculator (Python)
- TASK-008: Scoring categories API
- TASK-009: Leaderboard API
- TASK-019: Neo4j graph layer + network multiplier

## Definition of Done
- [ ] Score calculator passes all unit tests (including edge cases: 0, 1000, penalty floor)
- [ ] API returns score + breakdown + level for any user
- [ ] Leaderboard correctly ranks users
- [ ] Hidden factors never leak raw values — only buckets shown
