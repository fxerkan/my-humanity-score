# EPIC-009 — Platform Integrations

## Status: `blocked` (needs EPIC-002)
## Priority: P2 (Sprint 3)

## Goal
Connect external platforms (GitHub, LinkedIn, Twitter/X) via OAuth 2.0
to auto-import verified activities and feed the toxicity scorer.

## Scope
- OAuth 2.0 provider connections with token storage
- GitHub: open-source contributions, stars, repos
- LinkedIn: volunteer work, certifications, endorsements
- Twitter/X: public posts (toxicity analysis source)
- Sync frequency configuration per platform
- Manual re-sync trigger
- Activity import + deduplication

## Tasks
- TASK-018: OAuth 2.0 connections (GitHub + LinkedIn)

## Definition of Done
- [ ] User can connect GitHub and see imported contributions
- [ ] LinkedIn volunteer entries create pending activity claims
- [ ] Connected platform tokens stored encrypted
- [ ] Sync runs on configured schedule via Celery
