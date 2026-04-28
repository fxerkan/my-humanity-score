---
id: TASK-45
title: Seed Data Script
status: Done
assignee: []
created_date: '2026-04-27 17:00'
updated_date: '2026-04-28 12:03'
labels:
  - epic001-foundation
  - developer
  - haiku
  - pre-mvp
milestone: 'M4: Demo Integration'
dependencies:
  - task-2
  - task-7
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create a seed script that populates the database with 5 realistic demo users
and their activities so the Pre-MVP demo can show meaningful MHS scores without
requiring real user sign-up or activity submission.

## Demo Users to Create

| ID | Name | Profile | Expected Score Range |
|----|------|---------|---------------------|
| 1 | Elif Kaya | Environmental activist, teacher | 320–380 |
| 2 | Marcus Johnson | Open source developer, volunteer | 410–460 |
| 3 | Yuna Park | Artist, community organizer | 280–330 |
| 4 | Amir Hassan | Researcher, blood donor | 350–400 |
| 5 | Sofia Rossi | Entrepreneur, climate advocate | 370–420 |

## Seed Activities per User
Each user gets 3–8 activities spread across categories:
- Social Impact (volunteering, mentoring)
- Environmental (tree planting, carbon reduction)
- Knowledge & Innovation (open source, publications)
- Economic Contribution (job creation, donations)
- Cultural & Artistic (art, music, events)
- Civic & Political (voting, advocacy)

## Script Location
`scripts/seed_demo.py` — runs via `docker compose exec api python scripts/seed_demo.py`

## Technical Notes
- Use SQLAlchemy async session to insert rows
- Call the score calculator after inserting activities
- Store result in `mhs_scores` table
- Print summary table after completion
<!-- SECTION:DESCRIPTION:END -->

# TASK-045 — Seed Data Script

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Seed script created at scripts/seed_demo.py and apps/api/scripts/seed_demo.py. Inserts 5 realistic demo users (Elif Kaya, Marcus Johnson, Yuna Park, Amir Hassan, Sofia Rossi) with pre-computed MHS scores and category breakdowns. Idempotent — skips existing users. Verified by Gemini QA.
<!-- SECTION:FINAL_SUMMARY:END -->
