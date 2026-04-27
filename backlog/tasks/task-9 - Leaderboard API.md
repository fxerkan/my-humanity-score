---
id: TASK-9
assignee: []
title: "Leaderboard API"
status: To Do
priority: high
labels: ["epic003-mhs-scoring-engine", "haiku", "developer"]
dependencies:
  - task-8
acceptance_criteria:
  - "Only public profiles appear in leaderboards"
  - "Results cached in Redis with 5-minute TTL"
  - "Pagination works correctly (page, limit, total)"
  - "Private users are excluded even if they have high scores"
  - "Category filter returns correct ordering"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-003 MHS Scoring Engine
mhs_agent: Developer
mhs_model: claude-haiku-4-5
mhs_estimated_tokens: 15000
mhs_estimated_hours: 2
---

# TASK-009 — Leaderboard API

## Description
Paginated leaderboards: global, by country, and by category.
Only public profiles with `show_score=true` appear.

## Endpoints

### GET /leaderboard/global?page=1&limit=50
### GET /leaderboard/country/{country_code}?page=1&limit=50
### GET /leaderboard/category/{category}?page=1&limit=50

Response format:
```json
{
  "total": 1024,
  "page": 1,
  "limit": 50,
  "entries": [
    {
      "rank": 1,
      "username": "erkan",
      "display_name": "Erkan Çiftçi",
      "avatar_url": null,
      "final_score": 842,
      "level": { "name": "Humanity Champion", "emoji": "🌍" },
      "location": "Istanbul"
    }
  ]
}
```

## Implementation notes
- Cache leaderboard results in Redis (TTL: 5 minutes)
- Never include users with `profile_public=false` or `show_score=false`
- Rank is recalculated on each cache refresh, not stored
- Category leaderboard ranks by that category's contribution score

## Acceptance Criteria
- [ ] Only public profiles appear in leaderboards
- [ ] Results cached in Redis with 5-minute TTL
- [ ] Pagination works correctly (page, limit, total)
- [ ] Private users are excluded even if they have high scores
- [ ] Category filter returns correct ordering
