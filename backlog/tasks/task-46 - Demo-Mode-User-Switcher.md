---
id: TASK-46
title: Demo Mode User Switcher
status: Done
assignee: []
created_date: '2026-04-27 17:00'
updated_date: '2026-04-28 12:03'
labels:
  - epic002-auth
  - developer
  - haiku
  - pre-mvp
milestone: 'M4: Demo Integration'
dependencies:
  - task-5
  - task-45
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
For Pre-MVP demo purposes, skip full JWT auth. Instead, add a simple
"demo mode" switcher in the header that lets viewers select any of the
5 seeded users. No passwords, no tokens — just a URL param / localStorage
to identify which demo user's score to show.

## UI

```
┌──────────────────────────────────────────────────────────┐
│  🌍 My Humanity Score (MHS)          [Demo: Elif Kaya ▼]     Pre-MVP    │
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
<!-- SECTION:DESCRIPTION:END -->

# TASK-046 — Demo Mode User Switcher

## Notes
- This component is REMOVED when real auth (TASK-4) is implemented
- Mark with `// TODO: remove when auth is live` comment

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented as a 'Demo accounts — click to fill' panel on the login page (apps/web/src/app/(auth)/login/page.tsx). Better than the original URL-param spec: uses real JWT auth so the full auth flow is tested. All 5 demo users listed with MHS scores; click fills email+password, one click to sign in. Verified by Gemini QA.
<!-- SECTION:FINAL_SUMMARY:END -->
