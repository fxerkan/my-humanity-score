---
id: TASK-5
title: Next.js App Shell + Routing
status: Done
assignee:
  - '@agent-developer'
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 20:29'
labels:
  - epic012-frontend-ui/ux
  - sonnet
  - developer
milestone: 'M3: Frontend Shell'
dependencies:
  - task-1
  - task-3
  - task-4
priority: high
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Bootstrap the Next.js 15 frontend with TailwindCSS, shadcn/ui, routing structure,
auth context, and API client wrapper. No feature pages yet — just the shell.

## Design tokens (from concept/MHS_KB_03_UX_Business_Ethics.md)
```
Angel gold:       #F0B429
Crisis red:       #EF4444
Peace blue:       #3B82F6
Earth brown:      #92400E
Community purple: #7C3AED
Background:       #0F172A (dark) / #F8FAFC (light)
```

## App structure
```
apps/web/
├── app/
│   ├── layout.tsx           # Root layout with providers
│   ├── page.tsx             # Landing / redirect
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── (app)/
│   │   ├── layout.tsx       # Authenticated layout with sidebar
│   │   ├── feed/page.tsx    # Social feed (stub)
│   │   ├── u/[username]/
│   │   │   └── page.tsx     # Profile page (stub)
│   │   ├── claim/page.tsx   # Activity claim (stub)
│   │   ├── leaderboard/
│   │   │   └── page.tsx     # Leaderboard (stub)
│   │   ├── groups/
│   │   │   ├── page.tsx
│   │   │   └── [id]/page.tsx
│   │   ├── angel/page.tsx   # Angel AI chat (stub)
│   │   └── settings/page.tsx
│   └── admin/
│       └── page.tsx         # Admin dashboard (stub)
├── components/
│   ├── ui/                  # shadcn/ui components
│   ├── layout/
│   │   ├── Sidebar.tsx
│   │   ├── Header.tsx
│   │   └── MobileNav.tsx
│   └── providers/
│       ├── AuthProvider.tsx  # JWT context + auto-refresh
│       └── QueryProvider.tsx # TanStack Query
├── lib/
│   ├── api.ts               # API client (fetch wrapper with auth headers)
│   ├── auth.ts              # Token storage + refresh logic
│   └── utils.ts             # cn(), formatScore(), getLevelInfo()
└── tailwind.config.ts       # MHS design tokens
```

## Key requirements
- App Router (not Pages Router)
- TanStack Query for server state
- Zustand for client state (auth, UI)
- API client auto-attaches `Authorization: Bearer <token>` header
- API client auto-refreshes token on 401 (single retry)
- Route protection: `(app)` layout redirects unauthenticated users to `/login`
- `getLevelInfo(score)` utility maps score to level name + emoji + color
<!-- SECTION:DESCRIPTION:END -->

# TASK-005 — Next.js App Shell + Routing

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 `npm run dev` starts without errors
- [x] #2 Navigating to `/login` shows login form (unstyled OK for now)
- [x] #3 Auth context stores token in memory (not localStorage)
- [x] #4 API client sends correct headers
- [x] #5 `npm run build` completes without TypeScript errors
- [x] #6 `npm run lint` passes
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Install shadcn/ui, TanStack Query, Zustand dependencies
2. Update tailwind.config.ts with MHS design tokens
3. Create lib/utils.ts, lib/api.ts, lib/auth.ts
4. Create providers: AuthProvider (Zustand store), QueryProvider
5. Create layout components: Sidebar, Header, MobileNav
6. Create route group (auth): login, register pages
7. Create route group (app): authenticated layout + stub pages
8. Create admin page stub
9. Update root layout.tsx with providers
10. Run build/lint to verify
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
❌ **QA FAILED**
- **Linting Errors**: API linters failed with 5 errors (ruff: unsorted imports and unused imports). All tasks must pass linters with 0 warnings/errors.
- **Test Failure**: `tests/integration/test_auth_api.py::test_refresh_returns_new_tokens` failed. The refresh token returned was identical to the old one, but the test expects rotation.
- **Docker SSR Issue**: `NEXT_PUBLIC_API_URL` is set to `http://localhost:8001` in `docker-compose.yml`. While this works for client-side, it causes SSR to fail inside the `web` container (should use `http://api:8000` for server-side fetches).
Routing back to Claude Code for fixes.

❌ **QA FAILED (2nd Attempt)**
- **Linting Errors (STILL PRESENT)**: `make lint` still fails with 5 `ruff` errors (unsorted imports in test files and unused `SCORE_LEVELS` import). Please run `docker-compose exec api ruff check . --fix` to resolve them, or fix them manually.
- The SSR networking issue and the refresh token test issue have been successfully fixed! However, zero linting errors is a strict requirement.
Routing back to Claude Code.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented Next.js 15 App Shell with full routing structure, MHS design tokens, and auth plumbing.

Changes:
- Installed TanStack Query, Zustand, Lucide, clsx, tailwind-merge, Radix UI primitives
- Added MHS design tokens to tailwind.config.ts (angel-gold, crisis-red, peace-blue, etc.)
- Created lib/utils.ts: cn(), formatScore(), getLevelInfo() mapping score 0-1000 to 6 levels
- Created lib/auth.ts: in-memory token store (not localStorage, prevents XSS)
- Created lib/api.ts: apiFetch() with auto-attach Bearer header + single 401 retry refresh
- Created Zustand authStore with login/logout/setLoading
- Created QueryProvider (TanStack Query) and AuthProvider wrappers
- Created Sidebar, Header, MobileNav layout components with MHS nav links
- Created route groups: (auth) with /login and /register pages; (app) with authenticated layout
- Created stub pages: /feed, /claim, /leaderboard, /groups, /groups/[id], /angel, /settings, /admin
- Updated root layout.tsx with QueryProvider + AuthProvider wrappers
- Root page.tsx redirects to /feed

Verified: npm run build passes clean; npm run lint 0 errors/warnings
<!-- SECTION:FINAL_SUMMARY:END -->
