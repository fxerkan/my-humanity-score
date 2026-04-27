---
id: TASK-22
assignee: []
title: "Feed - Social Timeline API"
status: To Do
priority: medium
labels: ["epic007-social-feed-&-timeline", "haiku", "developer"]
dependencies:
  - task-4
  - task-19
acceptance_criteria:
  - "Private activities never appear in network or global feed"
  - "Global feed returns highest-impact activities first"
  - "Pagination works correctly across all 3 endpoints"
  - "Unauthenticated requests can access global feed"
  - "Network feed only shows content from followed users"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-007 Social Feed & Timeline
mhs_agent: Developer
mhs_model: claude-haiku-4-5
mhs_estimated_tokens: 15000
mhs_estimated_hours: 2
---

# TASK-022 — Feed / Social Timeline API

## Description
Paginated activity feed for personal timeline, network feed,
and global highlights. Respects activity visibility settings.

## Endpoints

### GET /feed/personal?page=1&limit=20
Own verified activities in reverse chronological order.

### GET /feed/network?page=1&limit=20
Activities from followed users (public/followers-only with follow).

### GET /feed/global?page=1&limit=20
Top verified activities globally (curated: high impact, recently verified).
No authentication required.

## Feed item format
```json
{
  "id": "...",
  "user": { "username": "erkan", "display_name": "Erkan", "avatar_url": null },
  "type": "humanitarian",
  "title": "Blood donation at Red Crescent",
  "category": "social_impact",
  "impact_score": 8.5,
  "verification_status": "verified",
  "activity_date": "2026-04-15",
  "badges_awarded": ["🩸"],
  "created_at": "2026-04-15T14:00:00Z"
}
```

## Privacy rules
- `visibility=private`: never in any feed
- `visibility=followers`: only in network feed for followers
- `visibility=public`: all feeds

## Caching
- Global feed cached in Redis (TTL: 2 minutes)
- Personal/network feeds not cached (real-time)

## Acceptance Criteria
- [ ] Private activities never appear in network or global feed
- [ ] Global feed returns highest-impact activities first
- [ ] Pagination works correctly across all 3 endpoints
- [ ] Unauthenticated requests can access global feed
- [ ] Network feed only shows content from followed users
