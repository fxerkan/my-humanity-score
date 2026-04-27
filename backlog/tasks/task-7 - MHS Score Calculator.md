---
id: TASK-7
milestone: "M2: Score Engine"
assignee: []
title: "MHS Score Calculator"
status: To Do
priority: high
labels: ["epic003-mhs-scoring-engine", "sonnet", "developer"]
dependencies:
  - task-2
acceptance_criteria:
  - "`MHSCalculator.calculate(user_id)` returns `ScoreResult` dataclass"
  - "`ScoreResult` includes: `final_score`, `level`, `category_scores`, `hidden_bucket` (not raw values)"
  - "Score of 0 for user with no activities"
  - "Score never exceeds 1000 or goes below 0"
  - "Carbon penalty correctly reduces score by 100 at 10,000+ kg CO2e"
  - "Hidden factors are stored in DB but never returned raw via API"
  - "Unit tests cover: zero score, max score, penalty edge cases, all 7 levels"
  - "100% test coverage on calculator module"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-003 MHS Scoring Engine
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 30000
mhs_estimated_hours: 3
---

# TASK-007 — MHS Score Calculator (Python)

## Description
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

## Acceptance Criteria
- [ ] `MHSCalculator.calculate(user_id)` returns `ScoreResult` dataclass
- [ ] `ScoreResult` includes: `final_score`, `level`, `category_scores`, `hidden_bucket` (not raw values)
- [ ] Score of 0 for user with no activities
- [ ] Score never exceeds 1000 or goes below 0
- [ ] Carbon penalty correctly reduces score by 100 at 10,000+ kg CO2e
- [ ] Hidden factors are stored in DB but never returned raw via API
- [ ] Unit tests cover: zero score, max score, penalty edge cases, all 7 levels
- [ ] 100% test coverage on calculator module
