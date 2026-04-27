# EPIC-012 — Frontend UI/UX

## Status: `blocked` (needs EPIC-001)
## Priority: P0 (Sprint 1 — shell only)

## Goal
Next.js 15 frontend with the full UX design system from
concept/MHS_KB_03_UX_Business_Ethics.md.

## Scope

### Design tokens (from KB_03)
- Angel gold: #F0B429
- Crisis red, Peace blue, Earth brown, Community purple
- TailwindCSS config + shadcn/ui component library

### Pages
- Auth: /register, /login, /oauth/callback
- Profile: /u/[username] — score, badges, activities
- Activity claim: /claim (5-step flow)
- Feed: /feed — social timeline
- Leaderboard: /leaderboard
- Groups: /groups, /groups/[id]
- Angel AI: /angel (chat interface)
- Settings: /settings (privacy, connected accounts)
- Admin: /admin (protected)

### Components
- MHS score ring + radar chart (6 categories)
- Badge grid with tooltips
- Activity card
- Angel AI chat widget
- Group card + challenge progress bar

## Tasks
- TASK-005: Next.js app shell + routing (Sprint 1)
- TASK-006: User profile page (Sprint 1)
- TASK-028: Score visualization (radar chart)
- TASK-029: Activity claim flow UI (5 steps)
- TASK-030: Badge showcase component
- TASK-031: Feed timeline page
- TASK-032: Group management UI
- TASK-902: Angel AI chat interface

## Definition of Done
- [ ] All pages render without hydration errors
- [ ] Design tokens match spec (checked with Storybook or visual test)
- [ ] Fully responsive (mobile + desktop)
- [ ] No accessibility violations (axe-core clean)
