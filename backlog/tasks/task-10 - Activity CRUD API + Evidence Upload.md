---
id: TASK-10
assignee: []
title: "Activity CRUD API + Evidence Upload"
status: To Do
priority: high
labels: ["epic004-activity-system-&-verification", "sonnet", "developer"]
dependencies:
  - task-3
  - task-2
acceptance_criteria:
  - "Activity creation returns immediately (verification is async)"
  - "Evidence upload validates file type and size"
  - "Users can only edit/delete their own activities"
  - "Status transitions are logged with timestamps"
  - "Verified activity triggers score recalculation via Celery"
  - "`visibility=private` activities not returned for other users"
  - "Integration test covers: create → upload evidence → check status"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-004 Activity System & Verification
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 35000
mhs_estimated_hours: 4
---

# TASK-010 — Activity CRUD API + Evidence Upload

## Description
Full CRUD for activity claims with evidence file upload.
Activities start as `pending` and move through the verification pipeline.

## Endpoints

### POST /activities
Create new activity claim.
```json
{
  "type": "humanitarian",
  "title": "Blood donation at Red Crescent",
  "description": "...",
  "evidence_url": "https://...",
  "category": "social_impact",
  "activity_date": "2026-04-15",
  "visibility": "public"
}
```
Returns created activity with `status: "pending"`.

### POST /activities/{id}/evidence
Upload evidence file (multipart/form-data).
- Accepted: PDF, JPG, PNG, max 10MB
- Stored in local volume (dev) / S3-compatible (prod)
- Triggers verification pipeline via Celery

### GET /activities?user_id=&status=&page=
List activities with filtering and pagination.

### GET /activities/{id}
Get single activity details.

### PATCH /activities/{id}
Update activity (only if still `pending`, only own activities).

### DELETE /activities/{id}
Soft-delete activity (only own activities or admin).

## Verification status flow
```
pending → auto_verified (if API check passes)
        → peer_review   (if needs community votes)
        → verified      (after sufficient votes)
        → rejected      (if evidence invalid)
```

## Acceptance Criteria
- [ ] Activity creation returns immediately (verification is async)
- [ ] Evidence upload validates file type and size
- [ ] Users can only edit/delete their own activities
- [ ] Status transitions are logged with timestamps
- [ ] Verified activity triggers score recalculation via Celery
- [ ] `visibility=private` activities not returned for other users
- [ ] Integration test covers: create → upload evidence → check status
