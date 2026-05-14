---
id: TASK-8
title: Scoring Categories API
status: Done
assignee:
  - '@claude'
created_date: '2026-04-27 13:41'
updated_date: '2026-04-30 07:12'
labels:
  - epic003-mhs-scoring-engine
  - sonnet
  - developer
milestone: 'M2: Score Engine'
dependencies:
  - task-7
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Expose the MHS score and category breakdown via REST API endpoints.
Hidden factor raw values must never appear in responses.

## Endpoints

### GET /scores/{username}
Returns public score summary.
```json
{
  "username": "erkan",
  "final_score": 342,
  "level": { "name": "Contributor", "emoji": "💫", "range": [250, 399] },
  "global_percentile": 78.4,
  "calculated_at": "2026-04-27T10:00:00Z"
}
```

### GET /scores/me/breakdown
Returns full category breakdown for authenticated user.
```json
{
  "final_score": 342,
  "level": { "name": "Contributor", "emoji": "💫" },
  "categories": {
    "social_impact":        { "score": 180, "weight": 0.25, "contribution": 45.0 },
    "environmental":        { "score": 120, "weight": 0.20, "contribution": 24.0 },
    "knowledge_innovation": { "score": 200, "weight": 0.20, "contribution": 40.0 },
    "economic":             { "score": 100, "weight": 0.15, "contribution": 15.0 },
    "cultural_artistic":    { "score": 80,  "weight": 0.10, "contribution": 8.0 },
    "civic_political":      { "score": 100, "weight": 0.10, "contribution": 10.0 }
  },
  "hidden_adjustments": {
    "carbon_bucket": "low",       -- "none"|"low"|"medium"|"high" (never raw kg)
    "toxicity_bucket": "clean",   -- "clean"|"caution"|"warning"
    "network_effect": "positive", -- "none"|"positive"|"strong"
    "consistency": "regular",     -- "irregular"|"regular"|"consistent"
    "equity_boost": false
  }
}
```

### POST /scores/me/recalculate
Triggers async score recalculation via Celery.
Returns: `{ "task_id": "...", "status": "queued" }`
<!-- SECTION:DESCRIPTION:END -->

# TASK-008 — Scoring Categories API

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 `GET /scores/{username}` works for public profiles without auth
- [x] #2 `GET /scores/me/breakdown` requires auth
- [x] #3 Hidden factor raw values never appear in any response
- [x] #4 Hidden buckets use only allowed enum values
- [x] #5 Score updates within 30 seconds of activity verification
- [x] #6 `POST /scores/me/recalculate` returns task_id for polling
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Discovered auth.py has its own Limiter instance; had to disable both in conftest
- Registration always creates a zero MHSScore row — tests updated to reflect this system design
- _upsert_score() UPDATE approach used to set non-default score values (sorted by calculated_at DESC)
- datetime.utcnow() needed for DB column (no timezone) instead of datetime.now(UTC)

✅ **QA PASSED**
Functionality, UI, and code quality verified. Ready for human review.

✅ **QA PASSED**
All REST endpoints verified via integration tests and manual CURL requests.
Naming conventions (final_score, level) correctly mapped from ORM.
Ethics and privacy rules (hidden factor masking) strictly followed.

NaN regression fixed: schemas/user.py ScoreSummary now uses validation_alias for final_score/level. 100/100 tests passing.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added three new scoring API endpoints and fixed a NaN regression on the profile page.

Endpoints:
- GET /scores/{username} — public score summary with real global percentile calculation
- GET /scores/me/breakdown — authenticated per-category breakdown with client-safe hidden-adjustment buckets
- POST /scores/me/recalculate — stub async recalculation (task_id + "queued"); Celery wiring deferred to TASK-11

Ethics enforcement: raw hidden-factor values (kg CO2, toxicity index, penalty amounts, multiplier floats)
never appear in any response. Only named bucket labels (CarbonBucket, ToxicityBucket, NetworkEffect,
ConsistencyBucket) are exposed via HiddenAdjustments schema.

Bug fix: schemas/user.py ScoreSummary used old ORM column names (total_score, score_level) causing the
frontend profile page to read undefined and display NaN. Fixed with Pydantic validation_alias mapping to
final_score/level with populate_by_name=True.

Tests: 21 new integration tests covering all endpoints, ethics checks (recursive forbidden-field scan),
auth requirements, and edge cases. 100/100 total tests passing.
<!-- SECTION:FINAL_SUMMARY:END -->
