---
id: TASK-25
assignee: []
title: "Peer Verification System"
status: To Do
priority: medium
labels: ["epic004-activity-system-&-verification", "sonnet", "developer"]
dependencies:
  - task-10
acceptance_criteria:
  - "3 reviewers assigned per activity from eligible pool"
  - "Users from same region/category excluded from reviewer pool"
  - "2/3 approval moves activity to `verified`"
  - "Timeout (72h) correctly escalates to Layer 4"
  - "Reviewer cannot vote on own activities"
  - "Reviewer reputation tracked and affects pool eligibility"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-004 Activity System & Verification
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 25000
mhs_estimated_hours: 3
---

# TASK-025 — Peer Verification System

## Description
Community voting system for activity verification (Layer 3 of the
verification pipeline). Active verified users review pending activities.

## Reviewer selection
- Pool: users with MHS score > 100 and at least 3 verified activities
- Sampled to avoid reviewer bias: no reviewers from same region + same category
- 3 reviewers assigned per activity
- Conflict of interest check: reviewer cannot review activities they inspired

## Voting
```
POST /peer-review/{activity_id}/vote
Body: { "decision": "approve" | "reject", "reason"?: "..." }
```
- 2/3 majority: `approved` → activity moves to `verified`
- 1/3 or less approve: `rejected`
- Timeout 72 hours: escalates to Layer 4 (org email)

## Reviewer UI data
```
GET /peer-review/queue        # My assigned reviews
GET /peer-review/{id}         # Activity + evidence for review
```

## Reviewer reputation
- Successful reviews (matching eventual outcome): +1 rep
- Wrong calls consistently: reviewer paused from review pool
- Reputation stored in `reviewer_reputation` table

## Database
```sql
CREATE TABLE peer_reviews (
  id UUID PRIMARY KEY,
  activity_id UUID REFERENCES activities(id),
  reviewer_id UUID REFERENCES users(id),
  decision VARCHAR(10),  -- approve|reject|abstain
  reason TEXT,
  reviewed_at TIMESTAMPTZ,
  assigned_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ  -- assigned_at + 72h
);
```

## Acceptance Criteria
- [ ] 3 reviewers assigned per activity from eligible pool
- [ ] Users from same region/category excluded from reviewer pool
- [ ] 2/3 approval moves activity to `verified`
- [ ] Timeout (72h) correctly escalates to Layer 4
- [ ] Reviewer cannot vote on own activities
- [ ] Reviewer reputation tracked and affects pool eligibility
