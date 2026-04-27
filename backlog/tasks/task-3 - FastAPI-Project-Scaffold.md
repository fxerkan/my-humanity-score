---
id: TASK-3
title: FastAPI Project Scaffold
status: In Progress
assignee:
  - '@developer'
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 15:06'
labels:
  - epic001-foundation-&-infrastructure
  - sonnet
  - developer
milestone: 'M1: Dev Environment'
dependencies:
  - task-1
  - task-2
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create the FastAPI project structure with all routers, middleware, dependency
injection, and OpenAPI configuration. No database wiring yet — that comes in TASK-004.

## Project structure
```
apps/api/
├── main.py              # FastAPI app factory
├── config.py            # Settings via pydantic-settings
├── dependencies.py      # get_db, get_current_user, etc.
├── middleware.py        # CORS, logging, rate limit
├── routers/
│   ├── __init__.py
│   ├── health.py        # GET /health
│   ├── auth.py          # /auth/* routes (stub)
│   ├── users.py         # /users/* routes (stub)
│   ├── scores.py        # /scores/* routes (stub)
│   ├── activities.py    # /activities/* routes (stub)
│   ├── leaderboard.py   # /leaderboard/* routes (stub)
│   ├── feed.py          # /feed/* routes (stub)
│   ├── groups.py        # /groups/* routes (stub)
│   └── admin.py         # /admin/* routes (stub)
├── models/              # SQLAlchemy ORM models (mirrors schema)
│   ├── user.py
│   ├── score.py
│   ├── activity.py
│   └── group.py
├── schemas/             # Pydantic request/response schemas
│   ├── user.py
│   ├── score.py
│   ├── activity.py
│   └── common.py        # Pagination, errors
├── services/            # Business logic layer
│   └── __init__.py
└── tests/
    ├── conftest.py
    └── test_health.py
```

## Key configuration
- CORS: allow `localhost:3000` in dev, configured via env in prod
- OpenAPI: title "My Humanity Score (MHS) API", version "1.0.0", docs at `/docs`
- Rate limiting: via `slowapi` middleware (100 req/min per IP by default)
- Request logging: structured JSON logs with request ID
- Error handling: global exception handler returning `{"error": "...", "code": "..."}`
- Lifespan: database connection pool init/teardown via `asyncpg` or `SQLAlchemy async`
<!-- SECTION:DESCRIPTION:END -->

# TASK-003 — FastAPI Project Scaffold

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 `GET /health` returns `{"status": "ok", "version": "1.0.0"}`
- [ ] #2 OpenAPI docs accessible at `GET /docs`
- [ ] #3 CORS headers present on responses to `localhost:3000`
- [ ] #4 All router stubs return `{"message": "not implemented"}` with HTTP 501
- [ ] #5 `pytest tests/test_health.py` passes
- [ ] #6 `mypy apps/api/` passes with no errors
- [ ] #7 `ruff check apps/api/` passes with no errors
<!-- AC:END -->
