---
id: TASK-27
assignee: []
title: "Admin Dashboard API"
status: To Do
priority: low
labels: ["epic010-admin-&-governance", "haiku", "developer"]
dependencies:
  - task-4
acceptance_criteria:
  - "Non-admin JWT returns HTTP 403 on all /admin/* routes"
  - "Suspended users cannot log in"
  - "Guardian event resolution logged with admin user ID"
  - "Stats endpoints return within 2 seconds (add indexes if needed)"
  - "Admin audit log is append-only (no deletes)"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-010 Admin & Governance
mhs_agent: Developer
mhs_model: claude-haiku-4-5
mhs_estimated_tokens: 20000
mhs_estimated_hours: 2
---

# TASK-027 — Admin Dashboard API

## Description
Protected admin API endpoints for platform management.
All endpoints require `role=admin` JWT claim.

## Endpoints

### User management
```
GET    /admin/users?search=&status=&page=    # Search users
GET    /admin/users/{id}                     # User detail
POST   /admin/users/{id}/suspend             # Suspend account
POST   /admin/users/{id}/reinstate           # Reinstate account
POST   /admin/users/{id}/anonymize           # GDPR hard delete
```

### Verification queue
```
GET    /admin/verifications?status=pending   # Ethics board queue
POST   /admin/verifications/{id}/approve     # Manual approve
POST   /admin/verifications/{id}/reject      # Manual reject
```

### Guardian events (Angel AI escalations)
```
GET    /admin/guardian-events?level=CRITICAL # CRITICAL threats
POST   /admin/guardian-events/{id}/resolve   # Mark resolved
```

### Platform stats
```
GET    /admin/stats/overview                 # User count, score distribution
GET    /admin/stats/activities               # Verification pipeline metrics
GET    /admin/stats/scores                   # Score histogram
```

### Bias audit
```
POST   /admin/bias-audit/run                 # Trigger manual audit
GET    /admin/bias-audit/history             # Past audit reports
```

## Access control
- `role=admin` claim in JWT required
- Admin users created via CLI seed script (no self-registration as admin)
- All admin actions logged to `admin_audit_log` table

## Acceptance Criteria
- [ ] Non-admin JWT returns HTTP 403 on all /admin/* routes
- [ ] Suspended users cannot log in
- [ ] Guardian event resolution logged with admin user ID
- [ ] Stats endpoints return within 2 seconds (add indexes if needed)
- [ ] Admin audit log is append-only (no deletes)
