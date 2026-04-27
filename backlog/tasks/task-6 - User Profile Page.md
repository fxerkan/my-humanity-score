---
id: TASK-6
milestone: "M4: Demo Integration"
assignee: []
title: "User Profile Page"
status: To Do
priority: high
labels: ["epic002-authentication-&-user-profiles", "sonnet", "developer"]
dependencies:
  - task-4
  - task-5
acceptance_criteria:
  - "New user profile shows score = 0 with level \"🌱 Awakening\""
  - "Category bars all show 0 for new user"
  - "Empty badge grid shows onboarding CTA"
  - "Own profile shows \"Edit profile\" button"
  - "Other user's profile shows \"Follow\" button"
  - "Page is server-side rendered (Next.js SSR) for SEO"
  - "og:image meta tag present for social sharing"
  - "Mobile responsive layout verified"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-002 Authentication & User Profiles
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 35000
mhs_estimated_hours: 4
---

# TASK-006 — User Profile Page

## Description
Implement the user profile page showing MHS score, level badge, 6-category
breakdown, badge grid, and activity history. New users show 0 score and empty
sections with helpful onboarding prompts.

## API endpoints to add (in `routers/users.py`)
- `GET /users/{username}` — public profile data
- `GET /users/me/score` — detailed score breakdown (authenticated)
- `GET /users/me/activities` — paginated activity list

## Profile page sections

### Score display
- Large circular MHS score ring (0–1000)
- Level badge with emoji + name (e.g., "🌱 Awakening")
- Percentile text: "Top X% globally"
- Last updated timestamp

### Category breakdown
- 6 mini progress bars (Social Impact, Environmental, Knowledge,
  Economic, Cultural, Civic)
- Percentage contribution of each category

### Badge grid
- Layer 1–3 badges earned (empty state: "Start your journey →")
- Click badge for criteria tooltip

### Activity history
- Paginated list of verified activities
- Empty state: "Log your first activity →" CTA

### Profile header
- Avatar (initials fallback), display name, username, location, bio
- "Edit profile" button if own profile
- "Follow" button if other user's profile (placeholder)

## Acceptance Criteria
- [ ] New user profile shows score = 0 with level "🌱 Awakening"
- [ ] Category bars all show 0 for new user
- [ ] Empty badge grid shows onboarding CTA
- [ ] Own profile shows "Edit profile" button
- [ ] Other user's profile shows "Follow" button
- [ ] Page is server-side rendered (Next.js SSR) for SEO
- [ ] og:image meta tag present for social sharing
- [ ] Mobile responsive layout verified
