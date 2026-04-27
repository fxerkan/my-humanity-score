# EPIC-010 — Admin & Governance

## Status: `blocked` (needs EPIC-002)
## Priority: P3 (Sprint 4)

## Goal
Admin tools, bias auditing, and the RFC/voting governance system for
community-driven algorithm changes.

## Scope

### Admin dashboard
- User management (suspend, reinstate, flag)
- Activity verification queue (review pending claims)
- Ethics board notification feed (CRITICAL threats from Angel AI)
- Platform health metrics

### Bias auditor
- BiasAuditor Python class: annual parity checks across gender, country, age
- Group score parity assertions (no protected characteristic correlates with score)
- Audit report generation → published to GitHub automatically

### RFC voting
- RFC creation (14-day comment period)
- Community review (7 days)
- Voting (7 days, quorum required)
- Automatic status transitions

## Tasks
- TASK-017: Bias auditor + parity checks
- TASK-026: RFC voting system
- TASK-027: Admin dashboard API

## Definition of Done
- [ ] Admin can view and act on verification queue
- [ ] BiasAuditor finds no statistically significant correlation between
      protected characteristics and MHS score in test data
- [ ] RFC lifecycle works end-to-end
- [ ] Audit report published to `/docs/bias-audit/` on completion
