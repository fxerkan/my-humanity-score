---
id: TASK-6
title: User Profile Page
status: Done
assignee:
  - '@agent-developer'
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 20:29'
labels:
  - epic002-authentication-&-user-profiles
  - sonnet
  - developer
milestone: 'M4: Demo Integration'
dependencies:
  - task-4
  - task-5
priority: high
ordinal: 1000
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
- [x] #1 New user profile shows score = 0 with level "🌱 Awakening"
- [x] #2 Category bars all show 0 for new user
- [x] #3 Empty badge grid shows onboarding CTA
- [x] #4 Own profile shows "Edit profile" button
- [x] #5 Other user's profile shows "Follow" button
- [x] #6 Page is server-side rendered (Next.js SSR) for SEO
- [x] #7 og:image meta tag present for social sharing
- [x] #8 Mobile responsive layout verified
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

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
❌ **QA FAILED**
- **SSR 500 Error**: The profile page returns a 500 Internal Server Error during SSR because it attempts to fetch from `localhost:8001` (from the `web` container perspective), which is unreachable. It must use `http://api:8000` or a shared environment variable that works for both client and server.
- **Dependency issue**: Task 6 depends on Task 5, and the networking issue in Task 5 prevents Task 6 from being fully verified in the integrated environment.
Routing back to Claude Code for fixes.

❌ **QA FAILED (2nd Attempt)**
- **Project Linting Failed**: While the SSR 500 error was successfully fixed and the profile page now renders correctly, the overall project build fails due to 5 `ruff` linting errors in the API tests (see Task 5 notes). A task cannot be marked Done if the main build/lint pipeline is broken.
Routing back to Claude Code to fix the linting errors.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented User Profile page (SSR) with score ring, category bars, badge grid, and activity history.

Backend changes (apps/api/):
- schemas/user.py: Added ScoreSummary and UserPublicResponse schemas
- routers/users.py: Added GET /users/me/score (authenticated score breakdown) and GET /users/me/activities (paginated); updated GET /users/{username} to return UserPublicResponse with embedded score snapshot

Frontend changes (apps/web/):
- app/(app)/u/[username]/page.tsx: SSR server component; fetches public profile via API; generateMetadata() for og:image; ZERO_SCORE fallback for new users with no score
- components/profile/ProfileHeader.tsx: Avatar with initials fallback; "Edit profile" for own profile; "Follow" button for other users
- components/profile/ScoreRing.tsx: SVG circular arc ring scaled 0-1000
- components/profile/CategoryBars.tsx: 6 mini progress bars with category weights
- components/profile/BadgeGrid.tsx: Empty-state onboarding CTA
- components/profile/ActivityList.tsx: Empty-state onboarding CTA

All 8 ACs satisfied; build and lint pass clean.
<!-- SECTION:FINAL_SUMMARY:END -->
