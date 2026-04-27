# EPIC-011 — ML/AI Services

## Status: `blocked` (needs EPIC-001)
## Priority: P1 (Sprint 2)

## Goal
Standalone ML microservices that feed into the scoring engine and
verification pipeline: toxicity analysis, carbon calculation, evidence OCR.

## Scope

### Toxicity analyzer
- Model: toxic-BERT (Unitary/toxic-bert on HuggingFace)
- Input: text string
- Output: toxicity index 0.0–1.0 + category labels
- Used by: Angel AI Guardian, platform sync scoring

### Carbon calculator
- API: Climatiq (climatiq.io)
- Input: flight segments or vehicle trips
- Output: kg CO2e
- Maps to carbon penalty: ≥10t = -100, 5-10t = -70, 1-5t = -40, <1t = 0
- Runs weekly via Celery for connected transport accounts

### Activity evidence verifier
- Certificate OCR: Tesseract or Google Vision API
- NGO API lookups (Idealist, VolunteerMatch, UN Volunteers)
- Government/education API checks (ORCID, CrossRef for academic)
- Returns: verified | unverified | needs_peer_review

## Tasks
- TASK-012: Toxicity analyzer (toxic-BERT)
- TASK-013: Carbon calculator (Climatiq)
- TASK-014: Activity evidence verifier (OCR + NGO API)

## Definition of Done
- [ ] Toxicity analyzer returns score in < 500ms for typical text
- [ ] Carbon calculator matches Climatiq reference values ± 5%
- [ ] Evidence verifier correctly validates a test NGO certificate
- [ ] All services have health check endpoints
