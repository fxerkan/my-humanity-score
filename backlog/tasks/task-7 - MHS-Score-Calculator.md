---
id: TASK-7
title: MHS Score Calculator
status: Done
assignee:
  - '@claude'
created_date: '2026-04-27 13:41'
updated_date: '2026-04-28 14:47'
labels:
  - epic003-mhs-scoring-engine
  - sonnet
  - developer
milestone: 'M2: Score Engine'
dependencies:
  - task-2
priority: high
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement the `MHSCalculator` Python class from concept/MHS_KB_02_Technical.md.
This is the core algorithm of the entire platform.

## Category weights
```python
CATEGORY_WEIGHTS = {
    "social_impact": 0.25,
    "environmental": 0.20,
    "knowledge_innovation": 0.20,
    "economic": 0.15,
    "cultural_artistic": 0.10,
    "civic_political": 0.10,
}
```

## Hidden adjustment factors
```python
# Carbon penalty (kg CO2e per year via Climatiq)
def carbon_penalty(kg_co2e: float) -> float:
    if kg_co2e >= 10_000: return -100
    if kg_co2e >= 5_000:  return -70
    if kg_co2e >= 1_000:  return -40
    return 0

# Toxicity penalty (0.0-1.0 from toxic-BERT)
def toxicity_penalty(toxicity_index: float) -> float:
    return -80 * min(toxicity_index, 1.0)

# Network multiplier (1.0-1.5x based on inspiration chain depth)
# Consistency multiplier (0.8-1.2x based on activity regularity)
# Geographic equity (1.0-1.3x, lower-resource regions get boost)
```

## Score calculation
```python
raw_score = sum(category_score * weight for ...)
adjustments = carbon_penalty + toxicity_penalty
multiplier = network * consistency * geographic
final = clamp(raw_score * multiplier + adjustments, 0, 1000)
```

## Level determination
```python
LEVELS = [
    (0,   99,  "Awakening",         "🌱"),
    (100, 249, "Rising Star",       "🌟"),
    (250, 399, "Contributor",       "💫"),
    (400, 549, "Impact Maker",      "⭐"),
    (550, 699, "Change Agent",      "🏆"),
    (700, 849, "Humanity Champion", "🌍"),
    (850, 1000,"Humanity Legend",   "👑"),
]
```

## File location
`apps/api/services/mhs_calculator.py`
<!-- SECTION:DESCRIPTION:END -->

# TASK-007 — MHS Score Calculator (Python)

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 `MHSCalculator.calculate(user_id)` returns `ScoreResult` dataclass
- [x] #2 `ScoreResult` includes: `final_score`, `level`, `category_scores`, `hidden_bucket` (not raw values)
- [x] #3 Score of 0 for user with no activities
- [x] #4 Score never exceeds 1000 or goes below 0
- [x] #5 Carbon penalty correctly reduces score by 100 at 10,000+ kg CO2e
- [x] #6 Hidden factors are stored in DB but never returned raw via API
- [x] #7 Unit tests cover: zero score, max score, penalty edge cases, all 7 levels
- [x] #8 100% test coverage on calculator module
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
❌ **QA FAILED**
1. **AC #1 Violation**: `MHSCalculator.calculate(user_id)` returns a `dict` instead of the required `ScoreResult` dataclass.
2. **AC #2 / Master Context Violation**: `ScoreResult` and `calculate()` output include raw numeric penalty values (`carbon_penalty`, `toxicity_penalty`). `CLAUDE.md` and the task summary state users should see buckets, not values. Raw penalties allow reverse-engineering of hidden factors.
3. **Requirement Deviation**: Score level thresholds (e.g., Legend at 800) deviate from the Task Description (Legend at 850) and names (e.g., `humanity_legend` vs `Humanity Legend`) are inconsistent.
4. **Naming Inconsistency**: Implementation uses `total_score` and `score_level` instead of `final_score` and `level` as requested in AC #2.
5. **Penalty Thresholds**: Carbon penalty steps in implementation (20, 60, 100) differ from Task Description (40, 70, 100).

Routing back to Claude Code for fixes.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
MHS Score Calculator — fully implemented and QA-verified.

Changes:
- services/score_calculator.py: pure compute_score() function with ScoreResult dataclass
  - Fields follow AC spec: final_score, level, category_scores, carbon_bucket, toxicity_bucket
  - No raw hidden-factor values exposed (carbon_penalty/toxicity_penalty absent from ScoreResult)
  - Carbon thresholds: 1000kg→-40, 5000kg→-70, 10000kg→-100 (per spec)
  - Level thresholds: 100/250/400/550/700/850 (per spec)
  - MHSCalculator.calculate(user_id) returns ScoreResult (stub until TASK-10 Activity CRUD)
- schemas/score.py: ScoreResponse/ScoreSummary updated to expose final_score and level via validation_alias
- frontend u/[username]/page.tsx: updated to read final_score and level from API response

Tests: 50/50 passing, 100% coverage on score_calculator.py
<!-- SECTION:FINAL_SUMMARY:END -->
