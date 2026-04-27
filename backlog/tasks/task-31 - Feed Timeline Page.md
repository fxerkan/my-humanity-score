---
id: TASK-31
assignee: []
title: "Feed Timeline Page"
status: To Do
priority: medium
labels: ["epic012-frontend-ui/ux", "haiku", "developer"]
dependencies:
  - task-5
  - task-22
acceptance_criteria:
  - "Tab switching loads correct feed data"
  - "Infinite scroll loads next page on reaching bottom"
  - "Activity cards show all fields correctly"
  - "Global tab accessible without login"
  - "Loading skeleton matches card dimensions (no layout shift)"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-012 Frontend UI/UX
mhs_agent: Developer
mhs_model: claude-haiku-4-5
mhs_estimated_tokens: 15000
mhs_estimated_hours: 2
---

# TASK-031 — Feed Timeline Page

## Description
Social feed page with tabs for Personal, Network, and Global timelines.
Infinite scroll with activity cards.

## Page structure
```
/feed
├── Tabs: [My Activities] [Network] [Global]
├── Activity card list (infinite scroll)
└── Empty states per tab
```

## Activity card
```
┌─────────────────────────────────────┐
│ @erkan · April 15                   │
│ 🩸 Blood Donation at Red Crescent   │
│ Category: Social Impact · +8.5 pts  │
│ ✅ Verified                         │
└─────────────────────────────────────┘
```

## Tab behavior
- **My Activities**: personal timeline, always available
- **Network**: requires at least 1 follow; empty state "Find people →"
- **Global**: public, no auth required, shows top impact activities

## Infinite scroll
- Load 20 items per page
- `useIntersectionObserver` on sentinel div at bottom
- Loading skeleton on fetch
- "All caught up" message at end

## Empty states
- My Activities: "You haven't logged any activities yet → [Log Activity]"
- Network: "Follow other users to see their contributions → [Explore]"
- Global: "No activities yet" (unlikely but handle it)

## Acceptance Criteria
- [ ] Tab switching loads correct feed data
- [ ] Infinite scroll loads next page on reaching bottom
- [ ] Activity cards show all fields correctly
- [ ] Global tab accessible without login
- [ ] Loading skeleton matches card dimensions (no layout shift)
