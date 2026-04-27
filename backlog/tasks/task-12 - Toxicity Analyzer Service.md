---
id: TASK-12
assignee: []
title: "Toxicity Analyzer Service"
status: To Do
priority: high
labels: ["epic011-ml/ai-services", "sonnet", "developer"]
dependencies:
  - task-3
acceptance_criteria:
  - "Returns toxicity index in < 500ms for typical text (< 512 tokens)"
  - "Model loaded at startup (not per-request)"
  - "Handles multilingual text (outputs score even if language mismatch)"
  - "Threat level correctly maps to Angel AI Guardian actions"
  - "Health check endpoint: `GET /health` includes model load status"
  - "Unit tests with known toxic/non-toxic samples cover all threat levels"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-011 ML/AI Services
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 25000
mhs_estimated_hours: 3
---

# TASK-012 — Toxicity Analyzer Service (toxic-BERT)

## Description
Standalone toxicity analysis microservice using the Unitary `toxic-bert`
model from HuggingFace. Used by Angel AI Guardian and platform content sync.

## Model
- HuggingFace: `unitary/toxic-bert`
- Labels: `toxic`, `severe_toxic`, `obscene`, `threat`, `insult`, `identity_hate`
- Output: toxicity index 0.0–1.0 (max across all labels)

## API (internal microservice)
```
POST /analyze/toxicity
Body: { "text": "...", "language"?: "en" }
Response: {
  "toxicity_index": 0.87,
  "labels": {
    "toxic": 0.87,
    "severe_toxic": 0.12,
    "obscene": 0.44,
    "threat": 0.05,
    "insult": 0.71,
    "identity_hate": 0.23
  },
  "threat_level": "HIGH"  -- NONE|LOW|MEDIUM|HIGH|CRITICAL
}
```

## Threat level mapping
- `toxicity_index` < 0.30: NONE
- 0.30–0.60: LOW (warn user)
- 0.60–0.85: MEDIUM (filter + warn)
- 0.85–0.95: HIGH (suspend + notify ethics board)
- > 0.95: CRITICAL (block + log + ethics board)

## File location
`apps/api/services/toxicity_analyzer.py`

## Acceptance Criteria
- [ ] Returns toxicity index in < 500ms for typical text (< 512 tokens)
- [ ] Model loaded at startup (not per-request)
- [ ] Handles multilingual text (outputs score even if language mismatch)
- [ ] Threat level correctly maps to Angel AI Guardian actions
- [ ] Health check endpoint: `GET /health` includes model load status
- [ ] Unit tests with known toxic/non-toxic samples cover all threat levels
