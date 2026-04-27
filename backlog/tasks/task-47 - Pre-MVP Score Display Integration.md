---
id: TASK-47
assignee: []
title: "Pre-MVP Score Display Integration"
status: To Do
priority: high
milestone: "M5: Pre-MVP Demo"
labels: ["epic012-frontend", "developer", "sonnet", "pre-mvp"]
dependencies:
  - task-6
  - task-8
  - task-46
acceptance_criteria:
  - "Profile page fetches real score from GET /api/v1/scores/{user_id}"
  - "6-category breakdown displayed as horizontal bars (recharts or plain CSS)"
  - "Total score (0-1000) shown prominently with level name and emoji"
  - "Loading skeleton shown while fetch is in progress"
  - "Error state shown if API is unreachable"
  - "Works end-to-end: docker compose up → browser → score visible"
created_date: '2026-04-27 17:00'
updated_date: '2026-04-27 17:00'
mhs_epic: EPIC-012 Frontend UI/UX
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 20000
mhs_estimated_hours: 2
---

# TASK-047 — Pre-MVP Score Display Integration

## Description
Wire the profile page (TASK-6) to the real scoring API (TASK-8) so that
selecting a demo user shows their actual computed MHS score and category
breakdown from the database. This is the final integration step for Pre-MVP.

## Score Display Layout

```
┌────────────────────────────────────────────┐
│  👤 Elif Kaya                              │
│  🌱 Awakening                              │
│                                            │
│  MHS Score: 342 / 1000                    │
│  ████████████████████░░░░░░░░░░░░░░░░  34% │
│                                            │
│  Category Breakdown:                       │
│  Social Impact     ████████░░░░  68/250    │
│  Environmental     ██████░░░░░░  54/200    │
│  Knowledge         ████░░░░░░░░  40/200    │
│  Economic          ███░░░░░░░░░  35/150    │
│  Cultural          ██░░░░░░░░░░  22/100    │
│  Civic             ███░░░░░░░░░  31/100    │
└────────────────────────────────────────────┘
```

## API Contract
`GET /api/v1/scores/{user_id}` response:
```json
{
  "user_id": 1,
  "total_score": 342,
  "level": "Awakening",
  "level_emoji": "🌱",
  "categories": {
    "social_impact": { "score": 68, "max": 250, "pct": 27 },
    "environmental": { "score": 54, "max": 200, "pct": 27 },
    "knowledge_innovation": { "score": 40, "max": 200, "pct": 20 },
    "economic": { "score": 35, "max": 150, "pct": 23 },
    "cultural_artistic": { "score": 22, "max": 100, "pct": 22 },
    "civic_political": { "score": 31, "max": 100, "pct": 31 }
  }
}
```

## Tech Notes
- Use TanStack Query for data fetching (staleTime: 60s for demo)
- Category colors from `MHS_COLORS` design tokens
- Simple `<progress>` or recharts `<BarChart>` — keep it minimal
- No SSR needed for Pre-MVP (client-side fetch is fine)
