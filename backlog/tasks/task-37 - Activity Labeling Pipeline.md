---
id: TASK-37
assignee: []
title: "Activity Labeling Pipeline"
status: To Do
priority: medium
labels: ["epic004-activity-system-&-verification", "opus", "data-analyst"]
dependencies:
  - task-10
acceptance_criteria:
  - "Export script produces valid JSON Lines with no PII fields"
  - "Auto-labeler correctly labels known-good and known-bad test activities"
  - "Validation script catches: forbidden fields, skewed distribution, duplicates"
  - "Dataset has balanced representation across all 5 activity categories"
  - "Label schema documented in `data/labels/README.md`"
  - "CI validates label schema on every push (schema test)"
  - "No user names, emails, or other PII in any label file"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-004 Activity System & Verification
mhs_agent: Data Analyst
mhs_model: claude-opus-4-6
mhs_estimated_tokens: 30000
mhs_estimated_hours: 3
---

# TASK-037 — Activity Labeling Pipeline

## Description

Build a labeled dataset pipeline for the activity verification ML model
(TASK-014). Activities need ground-truth labels to train the evidence verifier
and to evaluate its accuracy over time.

## Label schema (`data/labels/schema.json`)

```json
{
  "version": "1.0",
  "fields": {
    "activity_id": "UUID of the activity in DB",
    "label": "verified | unverified | needs_peer_review | rejected",
    "confidence": "high | medium | low",
    "evidence_type": "ngo_api | certificate | url | none",
    "labeler": "human | auto_api | auto_ocr",
    "labeled_at": "ISO 8601 timestamp",
    "notes": "optional free text — rationale"
  },
  "forbidden_fields": [
    "religion", "ethnicity", "race", "gender", "sexual_orientation",
    "nationality", "language", "disability", "political_affiliation",
    "economic_status"
  ]
}
```

## Dataset splits

- `data/labels/raw/` — exported unlabeled activities (JSON Lines)
- `data/labels/labeled/` — ground truth labels (JSON Lines, one per line)
- `data/labels/train/` — 80% training split
- `data/labels/eval/` — 20% evaluation split

## Labeling scripts

### `scripts/labeling/export_sample.py`
Exports N unlabeled activities to `data/labels/raw/YYYY-MM-DD-sample.jsonl`.
Stratified by category (equal representation per type).

### `scripts/labeling/auto_label.py`
Applies automatic labels to activities where confidence is high:
- Activity with confirmed NGO API match → `verified` / `high`
- Activity with no evidence at all → `needs_peer_review` / `high`
- Activity with expired URL → `unverified` / `high`

### `scripts/labeling/validate_labels.py`
Checks:
- No forbidden fields in label file
- Label distribution is not heavily skewed (> 80% one class → warning)
- All activity_ids exist in the DB
- No duplicate labels for same activity_id

## Output

- Labeled dataset at `data/labels/labeled/activities-YYYY-MM-DD.jsonl`
- Label stats report at `reports/labels/YYYY-MM-DD-label-stats.md`

## Acceptance Criteria

- [ ] Export script produces valid JSON Lines with no PII fields
- [ ] Auto-labeler correctly labels known-good and known-bad test activities
- [ ] Validation script catches: forbidden fields, skewed distribution, duplicates
- [ ] Dataset has balanced representation across all 5 activity categories
- [ ] Label schema documented in `data/labels/README.md`
- [ ] CI validates label schema on every push (schema test)
- [ ] No user names, emails, or other PII in any label file
