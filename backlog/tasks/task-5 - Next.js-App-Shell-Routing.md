---
id: TASK-5
title: Next.js App Shell + Routing
status: In Progress
assignee:
  - '@agent-developer'
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 17:30'
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
- [ ] #1 `npm run dev` starts without errors
- [ ] #2 Navigating to `/login` shows login form (unstyled OK for now)
- [ ] #3 Auth context stores token in memory (not localStorage)
- [ ] #4 API client sends correct headers
- [ ] #5 `npm run build` completes without TypeScript errors
- [ ] #6 `npm run lint` passes
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
