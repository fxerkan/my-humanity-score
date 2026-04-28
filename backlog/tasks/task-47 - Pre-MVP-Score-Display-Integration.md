---
id: TASK-47
title: Pre-MVP Score Display Integration
status: Done
assignee: []
created_date: '2026-04-27 17:00'
updated_date: '2026-04-28 12:03'
labels:
  - epic012-frontend
  - developer
  - sonnet
  - pre-mvp
milestone: 'M5: Pre-MVP Demo'
dependencies:
  - task-6
  - task-8
  - task-46
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
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
<!-- SECTION:DESCRIPTION:END -->

# TASK-047 — Pre-MVP Score Display Integration

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Profile page at /u/[username] fetches real MHS score from the API via SSR. ScoreRing.tsx renders animated SVG arc proportional to score/1000. CategoryBars.tsx shows 6 colour-coded category bars with point values. Verified live with Elif Kaya (342) and Marcus Johnson (438). Verified by Gemini QA.
<!-- SECTION:FINAL_SUMMARY:END -->
