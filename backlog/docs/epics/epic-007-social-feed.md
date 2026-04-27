# EPIC-007 — Social Feed & Timeline

## Status: `blocked` (needs EPIC-002, EPIC-003)
## Priority: P2 (Sprint 3)

## Goal
A privacy-respecting activity feed showing verified contributions from
the user's network and global highlights.

## Scope
- Personal timeline (user's own verified activities)
- Network feed (activities from followed users)
- Global highlights (top activities, new badge earners)
- Activity cards with: type, category, impact score, verification status
- Privacy controls: public/followers-only/private per activity
- Pagination + infinite scroll

## Tasks
- TASK-022: Feed/social timeline API
- TASK-031: Feed timeline page (frontend)

## Definition of Done
- [ ] Feed loads and paginates correctly
- [ ] Private activities are not visible to non-followers
- [ ] Activity cards display all required fields
