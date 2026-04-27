# EPIC-990 — Angel AI System

> **⏳ POST-MVP:** Bu epic, MVP tamamlandıktan sonra geliştirilecek. Tüm task'lar 900+ numaralarıyla işaretlenmiştir.

## Status: `deferred` (post-MVP — needs EPIC-003, EPIC-004, EPIC-011 first)

## Priority: P3 (Post-MVP)

## Goal

Implement Angel AI: a dual-module LLM-based Guardian (security) and
Mentor (guidance) system built on open-source models.

## Scope

### Guardian module

- Toxicity detection (toxic-BERT, threshold > 0.85 = HIGH threat)
- Hate speech detection (CRITICAL level → block + log + ethics board)
- PII detection and masking warnings
- Fake profile scoring (pattern analysis)
- Coordinated attack detection
- Threat level escalation: LOW → MEDIUM → HIGH → CRITICAL
- Automated responses per threat level

### Mentor module

- Monthly impact summary generation (score changes, category breakdown)
- Personalized next-action suggestions based on profile
- Motivation nudge notifications
- Similar-profile discovery
- New challenge recommendations

### Technical

- Built on Llama 3.3-70b or Mistral (local/open-source)
- REST API for Guardian checks + Mentor summaries
- Chat interface integration

## Tasks

- TASK-900: Angel AI Guardian module
- TASK-901: Angel AI Mentor module
- TASK-902: Angel AI chat interface (frontend)

## Definition of Done

- [ ] Guardian correctly flags HIGH threat toxicity (tested with adversarial inputs)
- [ ] CRITICAL threat triggers block + ethics board notification
- [ ] Mentor generates coherent monthly summary for a test user
- [ ] Chat interface renders Guardian warnings and Mentor messages
- [ ] No personally identifiable information leaks in logs
