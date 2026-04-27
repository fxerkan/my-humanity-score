---
id: TASK-36
assignee: []
title: "Data Quality Pipeline"
status: To Do
priority: medium
labels: ["epic004-activity-system-&-verification", "opus", "data-analyst"]
dependencies:
  - task-2
  - task-10
acceptance_criteria:
  - "Script runs without error against an empty database"
  - "Script detects injected bad data in each check category"
  - "Report Markdown file created in `reports/quality/`"
  - "Celery Beat job scheduled and verified running"
  - "CI runs quality checks against test database on every push"
  - "Zero tolerance checks (score out of range, hidden factor leak) cause CI failure"
  - "Report does NOT contain any individual user PII (only counts + percentages)"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-004 Activity System & Verification
mhs_agent: Data Analyst
mhs_model: claude-opus-4-6
mhs_estimated_tokens: 35000
mhs_estimated_hours: 4
---

# TASK-036 — Data Quality Pipeline

## Description

Build an automated data quality pipeline that runs checks on all core tables
(users, activities, mhs_scores) and outputs a structured health report.
This is the foundation of master data management for the platform.

## Quality dimensions to check

### Activities table

| Check | Query | Threshold |
|---|---|---|
| Missing evidence | `evidence_url IS NULL AND evidence_file_path IS NULL` | < 30% of pending |
| Stuck in pending | `status = 'pending' AND created_at < NOW() - INTERVAL '7 days'` | 0 |
| Invalid dates | `activity_date > NOW() OR activity_date < '2000-01-01'` | 0 |
| Category mismatch | subcategory not in valid set for type | 0 |
| Duplicate submissions | same user_id + title + activity_date | 0 |

### Users table

| Check | Query | Threshold |
|---|---|---|
| Orphaned scores | mhs_scores with no matching user | 0 |
| Invalid birth year | `birth_year < 1900 OR birth_year > YEAR(NOW())` | 0 |
| Soft-deleted but active tokens | deleted_at IS NOT NULL + active platform token | 0 |

### mhs_scores table

| Check | Condition | Threshold |
|---|---|---|
| Score out of range | `final_score < 0 OR final_score > 1000` | 0 (hard stop) |
| Hidden factor leak | raw multiplier values in API response schemas | Must be 0 |
| Stale scores | `calculated_at < NOW() - INTERVAL '48 hours'` for active users | < 5% |

## Output

Reports saved to `reports/quality/YYYY-MM-DD-data-quality.md` with:

- Executive summary table (dimension → count → status)
- Detailed breakdown per failing check
- Recommended remediation actions
- Trend vs. previous report (delta)

## Script location

`scripts/quality/run_data_quality.py` — runnable standalone and via Celery

## Celery schedule

Weekly: every Monday at 01:00 UTC (added to `celery_app.py` beat schedule)

## Acceptance Criteria

- [ ] Script runs without error against an empty database
- [ ] Script detects injected bad data in each check category
- [ ] Report Markdown file created in `reports/quality/`
- [ ] Celery Beat job scheduled and verified running
- [ ] CI runs quality checks against test database on every push
- [ ] Zero tolerance checks (score out of range, hidden factor leak) cause CI failure
- [ ] Report does NOT contain any individual user PII (only counts + percentages)
