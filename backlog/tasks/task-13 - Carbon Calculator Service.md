---
id: TASK-13
assignee: []
title: "Carbon Calculator Service"
status: To Do
priority: high
labels: ["epic011-ml/ai-services", "sonnet", "developer"]
dependencies:
  - task-3
acceptance_criteria:
  - "Matches Climatiq reference values ± 5%"
  - "Handles Climatiq API timeout gracefully (cached last value, not 0)"
  - "`CLIMATIQ_API_KEY` missing → service returns error, score calculator uses penalty=0"
  - "Unit tests mock Climatiq API (no external calls in CI)"
  - "Bucket values match the 4 penalty tiers exactly"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-011 ML/AI Services
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 20000
mhs_estimated_hours: 2
---

# TASK-013 — Carbon Calculator Service (Climatiq)

## Description
Carbon footprint calculation service using the Climatiq API.
Feeds the carbon penalty hidden factor in the MHS score calculator.

## Climatiq API integration
- Endpoint: `https://api.climatiq.io/data/v1/estimate`
- Supported sources:
  - Flight: IATA airport codes, cabin class, passengers
  - Vehicle: distance + fuel type
  - Accommodation: hotel nights + location

## Internal API
```
POST /calculate/carbon
Body: {
  "activities": [
    { "type": "flight", "from": "IST", "to": "LHR", "cabin": "economy", "passengers": 1 },
    { "type": "vehicle", "distance_km": 15000, "fuel_type": "petrol" }
  ]
}
Response: {
  "total_kg_co2e": 2840.5,
  "breakdown": [...],
  "penalty": -40,
  "bucket": "medium"
}
```

## Penalty mapping
```python
def carbon_penalty(kg: float) -> tuple[int, str]:
    if kg >= 10_000: return -100, "critical"
    if kg >= 5_000:  return -70,  "high"
    if kg >= 1_000:  return -40,  "medium"
    return 0, "low"
```

## Celery job
- Runs weekly for users with connected transport accounts
- Also triggered manually via `POST /scores/me/recalculate`

## Acceptance Criteria
- [ ] Matches Climatiq reference values ± 5%
- [ ] Handles Climatiq API timeout gracefully (cached last value, not 0)
- [ ] `CLIMATIQ_API_KEY` missing → service returns error, score calculator uses penalty=0
- [ ] Unit tests mock Climatiq API (no external calls in CI)
- [ ] Bucket values match the 4 penalty tiers exactly
