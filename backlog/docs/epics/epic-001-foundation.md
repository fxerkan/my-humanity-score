# EPIC-001 — Foundation & Infrastructure

## Status: `ready`

## Priority: P0 (Sprint 1)

## Goal

Establish a working monorepo, containerized dev environment, and CI pipeline
that all subsequent epics depend on.

Use the CCPM (automazeio) to NLP based epic, feature management orchestration

and `Backlog.md` — Task Store (Markdown-native) task management approach.

## Scope

- Monorepo structure (apps/web, apps/api, packages/shared)
- Docker Compose: Next.js, FastAPI, PostgreSQL, Redis, Neo4j
- GitHub Actions: lint + typecheck + test + build
- Environment variable management (.env.example)
- Celery + Redis worker setup
- **Backlog.md** task management (installed, configured, browser on :6420)
- **CCPM** skill for spec-driven feature delivery (PRD → GitHub Issues → Agents)

## Tasks

### Development Infrastructure

- TASK-001: Repo setup + Docker + CI
- TASK-002: PostgreSQL schema + Alembic migrations
- TASK-003: FastAPI project scaffold
- TASK-020: Celery + Redis background jobs
- TASK-034: Unit + integration test suite
- TASK-035: E2E tests (Playwright)

### Project Management Tooling ✅

- TASK-042: Backlog.md installation and configuration ✅
- TASK-043: CCPM skill setup ✅
- TASK-044: Backlog migration from old format ✅

## Definition of Done

- [ ] `docker compose up` starts all services without errors
- [ ] CI pipeline passes on GitHub for every push
- [ ] No secrets committed to repo
- [ ] `README.md` documents how to run locally
- [x] `backlog browser` starts on port 6420 and shows all tasks
- [x] CCPM skill available at `~/.claude/skills/ccpm`
- [x] Backlog MCP registered in Claude Code (`claude mcp list` shows backlog)
