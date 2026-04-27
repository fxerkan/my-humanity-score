---
id: TASK-1
title: Repo Setup + Docker + CI
status: Done
assignee:
  - developer
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 16:45'
labels:
  - epic001-foundation-&-infrastructure
  - sonnet
  - developer
milestone: 'M1: Dev Environment'
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Bootstrap the monorepo structure, Docker Compose dev environment, and
GitHub Actions CI pipeline. This is the first task every other task depends on.

## Deliverables

### Monorepo structure
```
my-humanity-score/
├── apps/
│   ├── web/          # Next.js 15
│   └── api/          # FastAPI
├── packages/
│   └── shared/       # Shared types, utilities
├── docker/
│   ├── web.Dockerfile
│   ├── api.Dockerfile
│   └── neo4j/
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
├── .gitignore
├── .claudeignore     # skip node_modules, dist, .next
└── Makefile          # dev shortcuts
```

### Docker Compose services
- `web`: Next.js 15 (port 3000)
- `api`: FastAPI (port 8000, hot reload)
- `postgres`: PostgreSQL 16 (port 5432)
- `redis`: Redis 7 (port 6379)
- `neo4j`: Neo4j 5 (ports 7474, 7687)
- `worker`: Celery worker (same image as api)

### GitHub Actions CI (`.github/workflows/ci.yml`)
- Trigger: push to any branch, PR to main
- Jobs: lint (ruff + eslint), typecheck (mypy + tsc), test (pytest + jest), build
- Uses matrix strategy for fast feedback

### .env.example
```
DATABASE_URL=postgresql://mhs:mhs@localhost:5432/mhs
REDIS_URL=redis://localhost:6379/0
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=
JWT_SECRET=
CLIMATIQ_API_KEY=
ANGEL_AI_MODEL=llama3.3-70b
```
<!-- SECTION:DESCRIPTION:END -->

# TASK-001 — Repo Setup + Docker + CI

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 `docker compose up` starts all 6 services without errors
- [x] #2 `make dev` alias works
- [x] #3 FastAPI health check at `GET /health` returns `{"status": "ok"}`
- [x] #4 Next.js renders index page at `localhost:3000`
- [x] #5 GitHub Actions CI pipeline exists and passes on empty scaffold
- [x] #6 `.env.example` documents all required environment variables
- [x] #7 `.claudeignore` excludes `node_modules`, `dist`, `.next`, `__pycache__`
- [x] #8 No secrets in git history
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
QA by Gemini (2026-04-27): PASS. Migration trigger bug fixed (mhs_scores excluded from updated_at loop). README ports corrected. Docker profiles documented.
<!-- SECTION:NOTES:END -->

## Notes
- Use `python:3.12-slim` base for API Dockerfile
- Use `node:20-alpine` base for web Dockerfile
- Pin all dependency versions in docker-compose for reproducibility
- PostgreSQL data volume should be named (`postgres_data`) for persistence
