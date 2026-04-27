---
id: TASK-18
assignee: []
title: "OAuth 2.0 Platform Connections"
status: To Do
priority: medium
labels: ["epic009-platform-integrations", "sonnet", "developer"]
dependencies:
  - task-4
acceptance_criteria:
  - "GitHub OAuth flow completes without error in dev environment"
  - "Access tokens stored encrypted (verified: raw token not in DB)"
  - "GitHub repos imported as pending activities"
  - "Manual sync trigger queues Celery task"
  - "Disconnecting platform removes token + stops future syncs"
  - "OAuth state parameter used to prevent CSRF"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-009 Platform Integrations
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 35000
mhs_estimated_hours: 4
---

# TASK-018 — OAuth 2.0 Platform Connections (GitHub + LinkedIn)

## Description
Allow users to connect external platforms via OAuth 2.0.
Imported activities create pending claims for verification.

## Supported platforms (MVP)
- GitHub (contributions, repos, stars received)
- LinkedIn (volunteer experience, certifications)

## OAuth flow
```
1. User clicks "Connect GitHub"
2. GET /integrations/github/authorize → redirect to GitHub OAuth
3. GitHub redirects to GET /integrations/github/callback?code=...
4. Exchange code for access token (server-side)
5. Encrypt token, store in connected_platforms
6. Trigger initial sync Celery task
7. Redirect user to settings page
```

## GitHub data import
- Endpoint: `GET /user/repos`, `GET /user/events`
- Map to: knowledge_innovation category activities
- Create pending activity: "Open source contribution to {repo}"

## LinkedIn data import
- Endpoint: LinkedIn v2 API `/me/volunteer`
- Map to: social_impact category activities
- Create pending activity with volunteer org + dates

## Token security
- Access tokens encrypted with AES-256 before storage
- Encryption key from `ENCRYPTION_KEY` env var (min 32 bytes)
- Token refresh handled automatically on 401

## Endpoints
```
GET  /integrations                          # List connected platforms
GET  /integrations/{platform}/authorize     # Start OAuth flow
GET  /integrations/{platform}/callback      # OAuth callback
POST /integrations/{platform}/sync          # Manual re-sync trigger
DELETE /integrations/{platform}             # Disconnect platform
```

## Acceptance Criteria
- [ ] GitHub OAuth flow completes without error in dev environment
- [ ] Access tokens stored encrypted (verified: raw token not in DB)
- [ ] GitHub repos imported as pending activities
- [ ] Manual sync trigger queues Celery task
- [ ] Disconnecting platform removes token + stops future syncs
- [ ] OAuth state parameter used to prevent CSRF
