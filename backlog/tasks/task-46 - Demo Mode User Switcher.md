---
id: TASK-46
assignee: []
title: "Demo Mode User Switcher"
status: To Do
priority: high
milestone: "M4: Demo Integration"
labels: ["epic002-auth", "developer", "haiku", "pre-mvp"]
dependencies:
  - task-5
  - task-45
acceptance_criteria:
  - "Header shows a dropdown to switch between 5 demo users (no login required)"
  - "Selecting a user updates the profile view immediately"
  - "Selected user persisted in localStorage between page refreshes"
  - "Demo banner shown: 'Pre-MVP Demo — real auth coming soon'"
  - "Works without any JWT or session tokens"
created_date: '2026-04-27 17:00'
updated_date: '2026-04-27 17:00'
mhs_epic: EPIC-002 Authentication & User Profiles
mhs_agent: Developer
mhs_model: claude-haiku-4-5
mhs_estimated_tokens: 8000
mhs_estimated_hours: 1
---

# TASK-046 — Demo Mode User Switcher

## Description
For Pre-MVP demo purposes, skip full JWT auth. Instead, add a simple
"demo mode" switcher in the header that lets viewers select any of the
5 seeded users. No passwords, no tokens — just a URL param / localStorage
to identify which demo user's score to show.

## UI

```
┌──────────────────────────────────────────────────────────┐
│  🌍 Kindora          [Demo: Elif Kaya ▼]     Pre-MVP    │
└──────────────────────────────────────────────────────────┘
```

Dropdown options:
- Elif Kaya (ID: 1)
- Marcus Johnson (ID: 2)
- Yuna Park (ID: 3)
- Amir Hassan (ID: 4)
- Sofia Rossi (ID: 5)

## Implementation
- Store selected `userId` in `localStorage["demo_user_id"]`
- Pass as query param: `/profile?userId=1`
- No auth middleware — API accepts `?userId=N` for demo endpoints
- Wrap in `DemoModeProvider` context so all components can read current user

## Notes
- This component is REMOVED when real auth (TASK-4) is implemented
- Mark with `// TODO: remove when auth is live` comment
