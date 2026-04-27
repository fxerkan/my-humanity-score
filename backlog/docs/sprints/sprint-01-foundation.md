# Sprint 1 — Foundation

**Duration:** 2 weeks (Week 1–2)
**Goal:** Working dev environment + basic user profile with MHS display
**Status:** `planned`

---

## Tasks in this sprint (ordered)

### Phase 1 — Parallel start (Day 1)

These 3 tasks can start immediately with no dependencies:

| Task     | Description                 | Agent     | Model  | Est |
| -------- | --------------------------- | --------- | ------ | --- |
| TASK-001 | Repo setup + Docker + CI    | Developer | Sonnet | 3h  |
| TASK-003 | FastAPI project scaffold    | Developer | Sonnet | 2h  |
| TASK-005 | Next.js app shell + routing | Developer | Sonnet | 3h  |

> Run TASK-001 first (creates the monorepo structure), then TASK-003 and
> TASK-005 can start in parallel once the directories exist.

### Phase 2 — After TASK-001 + TASK-003 complete (Day 2)

| Task     | Description                 | Agent     | Model  | Est | Deps |
| -------- | --------------------------- | --------- | ------ | --- | ---- |
| TASK-002 | PostgreSQL schema + Alembic | Developer | Sonnet | 2h  | 001  |

> TASK-002 needs the Docker Compose PostgreSQL service from TASK-001.

### Phase 3 — After TASK-002 + TASK-003 complete (Day 3)

| Task     | Description               | Agent     | Model  | Est | Deps     |
| -------- | ------------------------- | --------- | ------ | --- | -------- |
| TASK-004 | JWT auth + refresh tokens | Developer | Sonnet | 4h  | 002, 003 |

### Phase 4 — After TASK-004 + TASK-005 complete (Day 4–5)

| Task     | Description       | Agent     | Model  | Est | Deps     |
| -------- | ----------------- | --------- | ------ | --- | -------- |
| TASK-006 | User profile page | Developer | Sonnet | 4h  | 004, 005 |

### Phase 5 — QA (Day 6, after all above complete)

| Task     | Description              | Agent  | Model | Est | Deps     |
| -------- | ------------------------ | ------ | ----- | --- | -------- |
| TASK-034 | Unit + integration tests | Tester | Haiku | 3h  | 001–006 |

---

## Execution commands

### TASK-001 (run first, alone)

```bash
claude "Read CLAUDE.md, AGENTS.md, .vibe/config.yml, and backlog/tasks/task-001-repo-setup-docker-ci.md.
Implement the full monorepo structure, Docker Compose dev environment
(Next.js, FastAPI, PostgreSQL, Redis, Neo4j, Celery services),
and GitHub Actions CI pipeline (lint + typecheck + test + build).
Follow all acceptance criteria exactly."
```

### TASK-003 + TASK-005 (parallel — 2 terminal windows, after TASK-001)

```bash
# Terminal 1:
claude "Read CLAUDE.md, AGENTS.md, and backlog/tasks/task-003-fastapi-scaffold.md.
Implement FastAPI project structure with all routers as stubs,
middleware, error handling, health check, CORS, OpenAPI config.
Do NOT touch the database yet — no DB wiring in this task."

# Terminal 2:
claude "Read CLAUDE.md, AGENTS.md, and backlog/tasks/task-005-nextjs-shell.md.
Implement Next.js 15 app shell: App Router structure, TailwindCSS + shadcn/ui,
layout components, auth context/provider, API client wrapper, design tokens
from concept/MHS_KB_03_UX_Business_Ethics.md."
```

### TASK-002 (after TASK-001 complete)

```bash
claude "Read CLAUDE.md, AGENTS.md, and backlog/tasks/task-002-database-schema.md.
Implement the full PostgreSQL schema (users, mhs_scores, activities,
connected_platforms, badges, groups tables) and Alembic migration files
exactly matching the spec in concept/MHS_KB_02_Technical.md.
Include indexes, triggers, and soft-delete pattern."
```

### TASK-004 (after TASK-002 + TASK-003 complete)

```bash
claude "Read CLAUDE.md, AGENTS.md, and backlog/tasks/task-004-authentication.md.
Implement JWT auth: register, login, refresh, logout, /auth/me endpoints.
Wire up to PostgreSQL users table from TASK-002 and FastAPI routers from TASK-003.
bcrypt password hashing, refresh token rotation via Redis, no email enumeration."
```

### TASK-005 continues in parallel with TASK-004

Already started in Phase 1.

### TASK-006 (after TASK-004 + TASK-005 complete)

```bash
claude "Read CLAUDE.md, AGENTS.md, and backlog/tasks/task-006-user-profile-page.md.
Implement the user profile page: MHS score ring (shows 0 for new users),
level badge (🌱 Awakening), 6-category breakdown, empty badge grid with CTA,
empty activity history. Connect to /users/{username} and /users/me/score APIs."
```

### TASK-034 (QA pass, after all Sprint 1 tasks complete)

```bash
claude "Read CLAUDE.md, AGENTS.md, and backlog/tasks/task-034-unit-integration-tests.md.
Write unit tests for MHS score calculator and auth service.
Write integration tests hitting the REAL PostgreSQL database (no mocks).
Target 80%+ overall coverage. Run tests and ensure all pass."
```

**Use model:** `claude-haiku-4-5` (cost optimization — `--model claude-haiku-4-5-20251001`)

---

## Definition of Done for Sprint 1

- [ ] `docker compose up` starts all services without errors
- [ ] `GET http://localhost:8000/health` returns `{"status": "ok"}`
- [ ] `http://localhost:3000` renders the Next.js app
- [ ] User can register via `POST /auth/register`
- [ ] User can log in and receive JWT tokens
- [ ] Profile page at `/u/{username}` shows score = 0 and "🌱 Awakening"
- [ ] JWT refresh flow works correctly
- [ ] CI pipeline passes on GitHub (lint + typecheck + test + build)
- [ ] No secrets committed to repo
- [ ] `pytest` passes with 80%+ coverage
- [ ] `npm run build` completes without TypeScript errors

---

## Token budget

| Task            | Estimated tokens   |
| --------------- | ------------------ |
| TASK-001        | ~30,000            |
| TASK-002        | ~20,000            |
| TASK-003        | ~25,000            |
| TASK-004        | ~35,000            |
| TASK-005        | ~25,000            |
| TASK-006        | ~35,000            |
| TASK-034        | ~25,000            |
| **Total** | **~195,000** |

**Recommended model:** `claude-sonnet-4-6` for TASK-001 through TASK-006
**Cost-optimized:** `claude-haiku-4-5-20251001` for TASK-034

---

## What comes after Sprint 1

Sprint 2 tasks (ready once Sprint 1 is done):

- TASK-007: MHS score calculator
- TASK-008: Scoring categories API
- TASK-010: Activity CRUD API
- TASK-012: Toxicity analyzer
- TASK-013: Carbon calculator
- TASK-020: Celery + Redis background jobs
