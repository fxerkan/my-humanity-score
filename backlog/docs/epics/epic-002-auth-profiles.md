# EPIC-002 — Authentication & User Profiles

## Status: `ready`
## Priority: P0 (Sprint 1)

## Goal
Users can register, log in, and view their profile with a starting MHS of 0.

## Scope
- JWT authentication with refresh token rotation
- OAuth 2.0 (GitHub, LinkedIn, Twitter/X) — handled in EPIC-009
- User registration + onboarding questionnaire
- Profile page: score display, badge grid (empty), activity history
- Privacy settings (public/private profile, hidden factors visibility)
- GDPR/KVKK compliance endpoints (export, erasure)

## Tasks
- TASK-004: JWT auth + refresh tokens
- TASK-006: User profile page
- TASK-021: GDPR/KVKK compliance endpoints

## Definition of Done
- [ ] User can register and log in
- [ ] JWT refresh flow works correctly
- [ ] Profile page renders with score = 0 for new users
- [ ] Data export and erasure endpoints work
