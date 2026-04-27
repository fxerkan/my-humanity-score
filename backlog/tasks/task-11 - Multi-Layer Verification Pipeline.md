---
id: TASK-11
assignee: []
title: "Multi-Layer Verification Pipeline"
status: To Do
priority: high
labels: ["epic004-activity-system-&-verification", "sonnet", "developer"]
dependencies:
  - task-10
acceptance_criteria:
  - "Pipeline runs asynchronously (non-blocking to the API)"
  - "Each layer result stored in `activity_verifications` table"
  - "Status webhook/notification sent on status change"
  - "`auto_verified` activities skip layers 3-5"
  - "Ethics board queue accessible via admin dashboard"
  - "Pipeline handles external API timeouts gracefully (retry + fallback)"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-004 Activity System & Verification
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 40000
mhs_estimated_hours: 5
---

# TASK-011 — Multi-Layer Verification Pipeline

## Description
Orchestrate the 5-layer verification pipeline as a Celery workflow.
Each layer gates the next; any layer can short-circuit to `rejected`.

## Verification layers

### Layer 1 — API check (automated, seconds)
- Query NGO APIs: Idealist, VolunteerMatch, UN Volunteers
- For academic: ORCID, CrossRef, Semantic Scholar
- For medical: blood bank APIs (where available)
- Result: `verified` → done | `unverified` → continue to layer 2

### Layer 2 — OCR + AI (automated, 10-30 seconds)
- Extract text from uploaded certificate/image via Tesseract
- AI validation: does the text match the claimed activity?
- Checks: organization name, date, signature presence
- Result: `verified` → done | `needs_review` → continue to layer 3

### Layer 3 — Peer review (community voting, 24-72 hours)
- Post to peer review queue
- 3 community members review (sampled from active verified users)
- 2/3 majority required for `verified`
- Timeout (72h): escalates to layer 4

### Layer 4 — Organization confirmation (email, 3-7 days)
- Email sent to organization listed in evidence
- Magic link for org to confirm/deny
- Timeout (7 days): escalates to layer 5

### Layer 5 — Ethics board review (manual, within 14 days)
- Manual review by ethics board member
- Used for: field duty (conflict zones), Nobel/awards, disputed claims
- Final decision is binding

## Celery task chain
```python
verify_activity.s(activity_id) | [
    layer1_api_check.s(),
    layer2_ocr_ai.s(),
    layer3_peer_review.s(),
    layer4_org_confirm.s(),
    layer5_ethics_board.s(),
]
```

## Acceptance Criteria
- [ ] Pipeline runs asynchronously (non-blocking to the API)
- [ ] Each layer result stored in `activity_verifications` table
- [ ] Status webhook/notification sent on status change
- [ ] `auto_verified` activities skip layers 3-5
- [ ] Ethics board queue accessible via admin dashboard
- [ ] Pipeline handles external API timeouts gracefully (retry + fallback)
