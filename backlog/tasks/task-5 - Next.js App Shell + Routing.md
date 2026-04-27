---
id: TASK-5
milestone: "M3: Frontend Shell"
assignee: []
title: "Next.js App Shell + Routing"
status: To Do
priority: high
labels: ["epic012-frontend-ui/ux", "sonnet", "developer"]
dependencies:
  - task-1
  - task-3
  - task-4
acceptance_criteria:
  - "`npm run dev` starts without errors"
  - "Navigating to `/login` shows login form (unstyled OK for now)"
  - "Auth context stores token in memory (not localStorage)"
  - "API client sends correct headers"
  - "`npm run build` completes without TypeScript errors"
  - "`npm run lint` passes"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-012 Frontend UI/UX
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 25000
mhs_estimated_hours: 3
---

# TASK-005 — Next.js App Shell + Routing

## Description
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

## Acceptance Criteria
- [ ] `npm run dev` starts without errors
- [ ] Navigating to `/login` shows login form (unstyled OK for now)
- [ ] Auth context stores token in memory (not localStorage)
- [ ] API client sends correct headers
- [ ] `npm run build` completes without TypeScript errors
- [ ] `npm run lint` passes
