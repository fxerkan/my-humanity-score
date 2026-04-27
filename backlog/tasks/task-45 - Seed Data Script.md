---
id: TASK-45
assignee: []
title: "Seed Data Script"
status: To Do
priority: high
milestone: "M4: Demo Integration"
labels: ["epic001-foundation", "developer", "haiku", "pre-mvp"]
dependencies:
  - task-2
  - task-7
acceptance_criteria:
  - "python scripts/seed_demo.py creates 5 demo users in the DB"
  - "Each user has 3-8 seeded activities across at least 3 score categories"
  - "MHS score calculated and stored for each user after seed"
  - "Script is idempotent (safe to run multiple times)"
  - "README documents how to run: docker compose exec api python scripts/seed_demo.py"
created_date: '2026-04-27 17:00'
updated_date: '2026-04-27 17:00'
mhs_epic: EPIC-001 Foundation & Infrastructure
mhs_agent: Developer
mhs_model: claude-haiku-4-5
mhs_estimated_tokens: 10000
mhs_estimated_hours: 1
---

# TASK-045 — Seed Data Script

## Description
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
