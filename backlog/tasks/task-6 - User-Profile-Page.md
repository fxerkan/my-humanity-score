---
id: TASK-6
title: User Profile Page
status: In Progress
assignee:
  - '@agent-developer'
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 17:30'
labels:
  - epic002-authentication-&-user-profiles
  - sonnet
  - developer
milestone: 'M4: Demo Integration'
dependencies:
  - task-4
  - task-5
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
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
<!-- SECTION:DESCRIPTION:END -->

# TASK-006 — User Profile Page

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 New user profile shows score = 0 with level "🌱 Awakening"
- [ ] #2 Category bars all show 0 for new user
- [ ] #3 Empty badge grid shows onboarding CTA
- [ ] #4 Own profile shows "Edit profile" button
- [ ] #5 Other user's profile shows "Follow" button
- [ ] #6 Page is server-side rendered (Next.js SSR) for SEO
- [ ] #7 og:image meta tag present for social sharing
- [ ] #8 Mobile responsive layout verified
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Extend users router: GET /users/me/score, GET /users/me/activities
2. Add UserPublicResponse schema with score embedded
3. Create profile page (SSR) at app/(app)/u/[username]/page.tsx
4. Build ScoreRing, CategoryBar, BadgeGrid, ActivityList components
5. Add getLevelInfo() to lib/utils.ts
6. Add og:image meta tags
7. Ensure mobile responsive with Tailwind
8. Verify all ACs
<!-- SECTION:PLAN:END -->
