---
id: TASK-26
assignee: []
title: "RFC Voting System"
status: To Do
priority: low
labels: ["epic010-admin-&-governance", "sonnet", "developer"]
dependencies:
  - task-23
acceptance_criteria:
  - "RFC lifecycle auto-advances on schedule via Celery Beat"
  - "Only eligible users (score ≥ 100) can vote"
  - "Quorum check enforced before result counted"
  - "Anonymous until voting closes (votes not visible before)"
  - "Accepted RFC creates GitHub issue for implementation"
  - "Email notification to author on status change"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-010 Admin & Governance
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 30000
mhs_estimated_hours: 3
---

# TASK-026 — RFC Voting System (Community Governance)

## Description
Community governance via RFC (Request for Comments) process.
Algorithm changes, policy updates, and new badge criteria go through RFC.

## RFC lifecycle (28 days total)
```
DRAFT → OPEN (14-day comment) → REVIEW (7-day) → VOTING (7-day) → ACCEPTED|REJECTED
```

## RFC types
- `algorithm_change`: scoring weight adjustments
- `badge_criteria`: new/modified badge requirements
- `policy`: platform policy changes
- `feature`: major new feature proposals

## Endpoints
```
POST /rfcs                          # Create RFC (any user)
GET  /rfcs?status=&type=&page=      # List RFCs
GET  /rfcs/{id}                     # RFC detail + comments + votes
POST /rfcs/{id}/comments            # Add comment (open phase)
POST /rfcs/{id}/vote                # Vote (voting phase only)
PATCH /rfcs/{id}/status             # Admin: advance phase
```

## Voting rules
- Eligible voters: users with MHS score ≥ 100
- Quorum: 100 votes minimum (or 1% of eligible users)
- Threshold: 60% approval for acceptance
- Anonymous voting (results revealed after voting closes)

## Database
```sql
CREATE TABLE rfcs (
  id UUID PRIMARY KEY,
  title VARCHAR(255),
  type VARCHAR(50),
  body TEXT,
  author_id UUID REFERENCES users(id),
  status VARCHAR(20) DEFAULT 'draft',
  opens_at TIMESTAMPTZ,
  review_at TIMESTAMPTZ,  -- opens_at + 14 days
  voting_at TIMESTAMPTZ,  -- review_at + 7 days
  closes_at TIMESTAMPTZ,  -- voting_at + 7 days
  result VARCHAR(20),
  yes_votes INTEGER DEFAULT 0,
  no_votes INTEGER DEFAULT 0
);
```

## Acceptance Criteria
- [ ] RFC lifecycle auto-advances on schedule via Celery Beat
- [ ] Only eligible users (score ≥ 100) can vote
- [ ] Quorum check enforced before result counted
- [ ] Anonymous until voting closes (votes not visible before)
- [ ] Accepted RFC creates GitHub issue for implementation
- [ ] Email notification to author on status change
