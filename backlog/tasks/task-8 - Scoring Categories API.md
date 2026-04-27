---
id: TASK-8
milestone: "M2: Score Engine"
assignee: []
title: "Scoring Categories API"
status: To Do
priority: high
labels: ["epic003-mhs-scoring-engine", "sonnet", "developer"]
dependencies:
  - task-7
acceptance_criteria:
  - "`GET /scores/{username}` works for public profiles without auth"
  - "`GET /scores/me/breakdown` requires auth"
  - "Hidden factor raw values never appear in any response"
  - "Hidden buckets use only allowed enum values"
  - "Score updates within 30 seconds of activity verification"
  - "`POST /scores/me/recalculate` returns task_id for polling"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-003 MHS Scoring Engine
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 20000
mhs_estimated_hours: 2
---

# TASK-008 — Scoring Categories API

## Description
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

## Acceptance Criteria
- [ ] `GET /scores/{username}` works for public profiles without auth
- [ ] `GET /scores/me/breakdown` requires auth
- [ ] Hidden factor raw values never appear in any response
- [ ] Hidden buckets use only allowed enum values
- [ ] Score updates within 30 seconds of activity verification
- [ ] `POST /scores/me/recalculate` returns task_id for polling
