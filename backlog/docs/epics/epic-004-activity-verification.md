# EPIC-004 — Activity System & Verification

## Status: `blocked` (needs EPIC-001, EPIC-002)
## Priority: P1 (Sprint 2)

## Goal
Users can submit activity claims with evidence; a 5-layer pipeline verifies them.

## Scope
- 5 activity categories: Humanitarian, Science & Innovation, Community,
  Environment, Education
- Evidence types: URL, certificate/image (OCR), peer attestation, org API
- Verification layers: 1. API check → 2. OCR+AI → 3. Peer review →
  4. Organization confirmation → 5. Ethics board
- Activity CRUD with file upload (evidence)
- Peer verification (community voting)
- Special categories: field duty (Gaza/Ukraine/Sudan), Nobel/awards,
  patents, food waste, scholarships

## Tasks
- TASK-010: Activity CRUD API + evidence upload
- TASK-011: Multi-layer verification pipeline
- TASK-014: Activity evidence verifier (OCR + NGO API)
- TASK-025: Peer verification system

## Definition of Done
- [ ] User can submit an activity with evidence
- [ ] Verification pipeline runs all 5 layers in order
- [ ] Peer verification collects community votes
- [ ] Verified activities increase MHS score
