---
id: TASK-21
assignee: []
title: "GDPR-KVKK Compliance Endpoints"
status: To Do
priority: medium
labels: ["epic002-authentication-&-user-profiles", "haiku", "developer"]
dependencies:
  - task-4
acceptance_criteria:
  - "Export job completes and returns downloadable file"
  - "Soft-deleted users cannot log in"
  - "Hard anonymization removes all PII from all tables"
  - "Deletion can be cancelled within 30 days"
  - "Automated cleanup Celery job runs daily (deletes expired soft-deletes)"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-002 Authentication & User Profiles
mhs_agent: Developer
mhs_model: claude-haiku-4-5
mhs_estimated_tokens: 15000
mhs_estimated_hours: 2
---

# TASK-021 — GDPR/KVKK Compliance Endpoints

## Description
GDPR (EU) and KVKK (Turkey) compliance endpoints: data export, account
erasure with 30-day grace period, and data anonymization.

## Endpoints

### GET /users/me/export
- Triggers async job to package all user data as JSON
- Returns: `{ "job_id": "...", "estimated_minutes": 5 }`

### GET /users/me/export/{job_id}
- Check export status; when ready, returns signed download URL

### POST /users/me/delete
- Starts 30-day grace period (sets `deleted_at = now()`)
- Sends confirmation email
- Returns: `{ "deletion_date": "2026-05-27T10:00:00Z" }`

### POST /users/me/delete/cancel
- Cancels pending deletion (clears `deleted_at`)
- Only works within 30-day window

### POST /admin/users/{id}/anonymize
- Admin-only: hard anonymize (replace PII with `[DELETED]`)
- Used after 30-day grace period expires
- Preserves aggregate stats (score, activity counts) anonymized

## Data export package contents
- `user_profile.json`
- `activities.json`
- `mhs_scores_history.json`
- `connected_platforms.json` (no tokens)
- `badges.json`
- `groups.json`

## Acceptance Criteria
- [ ] Export job completes and returns downloadable file
- [ ] Soft-deleted users cannot log in
- [ ] Hard anonymization removes all PII from all tables
- [ ] Deletion can be cancelled within 30 days
- [ ] Automated cleanup Celery job runs daily (deletes expired soft-deletes)
