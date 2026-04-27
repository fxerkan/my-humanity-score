---
id: TASK-17
assignee: []
title: "Bias Auditor + Parity Checks"
status: To Do
priority: medium
labels: ["epic010-admin-&-governance", "sonnet", "developer"]
dependencies:
  - task-7
acceptance_criteria:
  - "`BiasAuditor.run()` completes without error on test dataset"
  - "Report correctly identifies injected bias in synthetic test data"
  - "Report correctly passes for unbiased synthetic test data"
  - "GitHub publish creates file in `docs/bias-audit/YYYY-QQ.md`"
  - "Audit log stored in `bias_audit_runs` table"
  - "Admin can trigger manually via `POST /admin/bias-audit/run`"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-010 Admin & Governance
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 25000
mhs_estimated_hours: 3
---

# TASK-017 — Bias Auditor + Parity Checks

## Description
Implement the `BiasAuditor` class that runs statistical parity checks
across protected characteristics. Results published to GitHub automatically.

## Protected characteristics to audit
From CLAUDE.md `FORBIDDEN_FEATURES`:
- Gender (if voluntarily provided)
- Country (from location field)
- Age group (from birth_year)

## Statistical tests
```python
class BiasAuditor:
    def run_parity_check(self, characteristic: str) -> PurityReport:
        # Group users by characteristic value
        # Compute mean MHS score per group
        # Run Kruskal-Wallis H-test (non-parametric ANOVA)
        # Flag if any group differs by > 15% from global mean
        # Compute effect size (Cohen's d for binary, eta-squared for multi)
```

## Report format
```markdown
# MHS Bias Audit Report — 2026-Q1

## Summary
- Total users audited: 15,234
- Protected characteristics checked: gender, country, age_group
- Issues found: 0

## Results by characteristic

### Gender
- Groups: [prefer_not_to_say, female, male, non_binary]
- Mean scores: [342, 338, 345, 340] (Δ max: 2.0%)
- Kruskal-Wallis p-value: 0.823 (no significant difference)
- ✅ PASS

### Country (top 20 by user count)
- ... (table)
- ✅ PASS

### Age group
- Groups: [18-25, 26-35, 36-50, 51+]
- ✅ PASS

## Conclusion: No statistically significant bias detected.
```

## Auto-publish to GitHub
- Uses `gh` CLI or PyGitHub to create/update file in `docs/bias-audit/`
- Runs annually via Celery cron (or triggered manually via admin)
- Creates a GitHub release with audit report as asset

## Acceptance Criteria
- [ ] `BiasAuditor.run()` completes without error on test dataset
- [ ] Report correctly identifies injected bias in synthetic test data
- [ ] Report correctly passes for unbiased synthetic test data
- [ ] GitHub publish creates file in `docs/bias-audit/YYYY-QQ.md`
- [ ] Audit log stored in `bias_audit_runs` table
- [ ] Admin can trigger manually via `POST /admin/bias-audit/run`
