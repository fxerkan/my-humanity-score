---
id: TASK-32
assignee: []
title: "Group Management UI"
status: To Do
priority: medium
labels: ["epic012-frontend-ui/ux", "sonnet", "developer"]
dependencies:
  - task-5
  - task-23
acceptance_criteria:
  - "Browse page filters work client-side (no page reload)"
  - "Create form validates slug format (lowercase, hyphens only)"
  - "Group detail tabs switch without full page reload"
  - "Challenge progress bar shows current/target count + time remaining"
  - "Join button changes to \"Leave\" after joining"
  - "Closed group shows \"Request to Join\" + pending state after request"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-012 Frontend UI/UX
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 30000
mhs_estimated_hours: 3
---

# TASK-032 — Group Management UI

## Description
Group browsing, creation, detail pages, and member management UI.

## Pages

### /groups — Browse groups
- Search bar + filters (type, theme, location)
- Group cards: name, type, member count, collective MHS, join button
- "Create group" button

### /groups/create — Create group
- Form: name, slug, description, type, theme, location, privacy
- Preview card as user types

### /groups/[id] — Group detail
- **Header**: group name, type badge, collective MHS score ring, member count
- **Tabs**: Feed | Members | Challenges | About
- **Feed tab**: group activity feed (TASK-031 component)
- **Members tab**: member list with individual MHS scores
- **Challenges tab**: active/past challenges with progress bars
- **About tab**: group description, rules, admin info
- **Join button**: "Join" (open) or "Request to Join" (closed)

### Challenge progress bar
```
🌱 May Green Month — Plant 100 trees
[████████████░░░░░░░░] 67/100 trees
14 days remaining
```

## State management
- Group data cached in TanStack Query (5-minute stale time)
- Optimistic join (show as joined immediately, revert on error)

## Acceptance Criteria
- [ ] Browse page filters work client-side (no page reload)
- [ ] Create form validates slug format (lowercase, hyphens only)
- [ ] Group detail tabs switch without full page reload
- [ ] Challenge progress bar shows current/target count + time remaining
- [ ] Join button changes to "Leave" after joining
- [ ] Closed group shows "Request to Join" + pending state after request
