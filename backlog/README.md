# Backlog.md — MHS Project Task Management Guide

> **Turkish version:** [README.tr.md](README.tr.md)

This guide covers how the My Humanity Score (My Humanity Score (MHS)) project uses **Backlog.md** for task management across all roles — Developer, Analyst, Tester, Data Crawler, Data Visualizer, and Reviewer.

---

## Table of Contents

1. [Directory Structure](#directory-structure)
2. [Core Concepts](#core-concepts)
3. [Daily CLI Reference by Role](#daily-cli-reference-by-role)
4. [Creating Epics](#creating-epics)
5. [Creating Tasks](#creating-tasks)
6. [Creating Draft Tasks](#creating-draft-tasks)
7. [Task Lifecycle](#task-lifecycle)
8. [Working with Documents and Decisions](#working-with-documents-and-decisions)
9. [Kanban Board and Browser](#kanban-board-and-browser)
10. [Dependency Management](#dependency-management)
11. [Task Templates](#task-templates)
12. [MHS Label Conventions](#mhs-label-conventions)
13. [AI Agent Integration](#ai-agent-integration)

---

## Directory Structure

```
backlog/
├── README.md                  ← This file (English)
├── README.tr.md               ← Turkish version
├── config.yml                 ← Backlog.md project configuration
│
├── tasks/                     ← All active tasks (flat, Markdown files)
│   ├── task-1 - Title.md
│   ├── task-2 - Title.md
│   └── task-900 - Title.md    ← Post-MVP tasks (900+ range)
│
├── drafts/                    ← Ideas not yet ready for development
│
├── docs/                      ← Reference documentation
│   ├── epics/                 ← Epic planning documents
│   │   ├── epic-001-foundation.md
│   │   ├── epic-002-auth-profiles.md
│   │   └── ...
│   └── sprints/               ← Sprint planning documents
│       └── sprint-01-foundation.md
│
├── decisions/                 ← Architecture Decision Records (ADRs)
│
├── milestones/                ← Milestone tracking
│
├── completed/                 ← Archived completed tasks
└── archive/                   ← Archived cancelled/deferred tasks
```

### Task Numbering Convention

| Range | Purpose |
|-------|---------|
| 1–99 | MVP Sprint 1 — Foundation & Infrastructure |
| 100–199 | MVP Sprint 2 — Core Features |
| 200–299 | MVP Sprint 3 — Advanced Features |
| 300–399 | MVP Sprint 4 — Polish & Launch |
| 400–499 | Data roles (Analyst, Crawler, Visualizer) |
| 900+ | **Post-MVP** — Angel AI, advanced governance |

---

## Core Concepts

| Concept | What it is | Where it lives |
|---------|-----------|----------------|
| **Task** | A single unit of work (1 session / 1 PR) | `backlog/tasks/task-N - Title.md` |
| **Draft** | An idea not yet ready for development | `backlog/drafts/` |
| **Epic** | A group of related tasks with a shared goal | `backlog/docs/epics/epic-NNN-*.md` |
| **Sprint** | A time-boxed set of tasks | `backlog/docs/sprints/sprint-NN-*.md` |
| **Decision** | An Architecture Decision Record (ADR) | `backlog/decisions/` |
| **Milestone** | A set of tasks grouped for a release | managed by `backlog milestone` |

**The golden rule:** One task = one agent session = one PR. If a task takes more than one session to complete, it should be split into subtasks.

---

## Daily CLI Reference by Role

### Everyone — Start of Day

```bash
# See everything at a glance
backlog board

# Open web UI (port 6420)
backlog browser

# See what's in progress
backlog task list --status "In Progress" --plain

# See what's ready to start (no blockers)
backlog sequence list --plain

# Search for something
backlog search "scoring"
```

---

### Developer

```bash
# Pick up the next task
backlog task list --status "To Do" --priority high --plain

# View a task in full detail
backlog task view 7

# Start working — move to In Progress
backlog task edit 7 --status "In Progress" --assignee "@me"

# Add implementation notes while coding
backlog task edit 7 --append-notes "Using SQLAlchemy 2 async session"

# Check off an acceptance criterion
backlog task edit 7 --check-ac 1

# Mark as done
backlog task edit 7 --status "Done"

# Create a subtask under a parent
backlog task create "Add index on activities.user_id" \
  --parent 2 \
  --priority high \
  --labels "epic001-foundation,database"

# Add a dependency
backlog task edit 8 --dep 7

# Archive a completed task
backlog task archive 7
```

---

### Analyst / Data Analyst

```bash
# List all data-quality tasks
backlog task list --plain | grep -i "quality\|label\|mdm"

# Search for data-related tasks
backlog search "data quality" --type task

# Create a quality check task
backlog task create "Run weekly data quality report" \
  --priority medium \
  --labels "epic011-ml-ai,data-analyst" \
  --ac "Quality report written to reports/quality/YYYY-MM-DD.md" \
  --ac "No zero-tolerance violations found"

# Create an Architecture Decision Record
backlog decision create "Use partitioned tables for activities at 10M rows"

# View the dependency execution order
backlog sequence list --plain

# Check what's blocked
backlog task list --plain | grep -i "blocked"
```

---

### Tester / QA

```bash
# Find tasks ready for testing
backlog task list --status "In Progress" --plain

# Create a test task linked to a feature
backlog task create "Test JWT auth edge cases" \
  --priority high \
  --labels "epic002-auth,tester" \
  --dep 4 \
  --ac "Login with wrong password returns 401 (not 403)" \
  --ac "Expired token returns 401 with refresh hint" \
  --ac "Refresh token works after 55-minute gap"

# Mark acceptance criteria as verified
backlog task edit 34 --check-ac 1 --check-ac 2

# Add a bug note
backlog task edit 34 --append-notes "BUG: refresh endpoint returns 500 when token is exactly expired"

# Create a draft for a bug report
backlog draft create "Bug: Score recalculation skips users with no activities"

# Promote draft bug to proper task
backlog draft promote 3
```

---

### Data Crawler

```bash
# See all crawler tasks
backlog task list --plain | grep -i "crawl\|integrat\|sync"

# Create a new crawler task
backlog task create "Add Idealist.org volunteer crawler" \
  --priority medium \
  --labels "epic009-integrations,data-crawler" \
  --ac "BaseCrawler subclass created in apps/api/crawlers/idealist.py" \
  --ac "Rate limit: 2 req/sec enforced" \
  --ac "robots.txt checked and respected" \
  --ac "Unit tests with mocked httpx responses pass"

# Document a crawler reference
backlog doc create "Idealist API Rate Limits" --path docs/integrations/idealist.md
```

---

### Data Visualizer

```bash
# See all visualization tasks
backlog task list --plain | grep -i "chart\|dashboard\|visual\|widget"

# Create a chart task
backlog task create "Category breakdown donut chart for public stats" \
  --priority medium \
  --labels "epic012-frontend,data-visualizer" \
  --ac "Uses recharts + MHS_COLORS design tokens" \
  --ac "Suppresses groups < 5 users (anonymization)" \
  --ac "Accessible: role=img, aria-label, figcaption"

# Export the board for a stakeholder update
backlog board export sprint1-status.md
```

---

### Reviewer / Tech Lead

```bash
# Full board overview
backlog board --milestones

# Check dependency chain for a task
backlog sequence list --plain

# View all high-priority items
backlog task list --priority high --plain

# Archive all tasks completed more than 30 days ago
backlog cleanup

# Export board snapshot
backlog board export --filename "$(date +%Y-%m-%d)-board-snapshot.md"

# Record an architecture decision
backlog decision create "Use Celery over FastAPI BackgroundTasks for score recalculation"
```

---

## Creating Epics

Epics are planning documents — they live in `backlog/docs/epics/` and are not managed by the `backlog` CLI directly. Create them as Markdown files following this template:

```bash
# Create a new epic doc
backlog doc create "EPIC-013 — Notification System" --path docs/epics/epic-013-notifications.md
```

### Epic Template

```markdown
# EPIC-NNN — [Epic Title]

## Status: `ready` | `in-progress` | `done` | `deferred`

## Priority: P0 (Sprint 1) | P1 (Sprint 2) | P2 (Sprint 3) | P3 (Post-MVP)

## Goal
[One paragraph: what this epic achieves and why it matters to MHS users.]

## Scope
- [Feature or deliverable 1]
- [Feature or deliverable 2]
- [Feature or deliverable 3]

## Out of Scope
- [Anything explicitly excluded to prevent scope creep]

## Tasks
- TASK-N: [Task title] — [Agent] — [Model] — [~Xh]

## Dependencies
- Requires EPIC-NNN (reason)

## Definition of Done
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] All tasks in this epic are Done
- [ ] No open bugs in scope
```

---

## Creating Tasks

### Via CLI (recommended for quick tasks)

```bash
backlog task create "Implement rate limiter middleware" \
  --priority high \
  --labels "epic001-foundation,developer,sonnet" \
  --dep 3 \
  --ac "All endpoints rate-limited at 100 req/min per IP" \
  --ac "429 response includes Retry-After header" \
  --ac "Rate limit config in settings.py (not hardcoded)"
```

### Via File (recommended for complex tasks)

Create `backlog/tasks/task-N - Title.md` manually using the template below.

### Task File Template

```markdown
---
id: TASK-N
assignee: []
title: "Short, imperative task title"
status: To Do
priority: high | medium | low
labels: ["epic00N-slug", "agent-role", "model-label"]
dependencies:
  - task-N
acceptance_criteria:
  - "Observable outcome 1 (user-facing or system-level)"
  - "Observable outcome 2"
created_date: 'YYYY-MM-DD HH:MM'
updated_date: 'YYYY-MM-DD HH:MM'
mhs_epic: EPIC-00N Title
mhs_agent: Developer | Analyst | Tester | Data Crawler | Data Visualizer
mhs_model: claude-sonnet-4-6 | claude-haiku-4-5 | claude-opus-4-7 | gemini-2.5-pro
mhs_estimated_tokens: 25000
mhs_estimated_hours: 2
---

# TASK-N — [Title]

## Description
[2–4 sentences explaining WHAT to build and WHY it matters to MHS.]

## Deliverables
[Specific files, endpoints, components, or scripts to be produced.]

## Technical Notes
[Implementation hints, key constraints, edge cases, or references to concept docs.]

## References
- [concept/MHS_KB_02_Technical.md — relevant section]
- [relevant ADR or external doc]
```

---

## Creating Draft Tasks

Use drafts for ideas that aren't fully specified yet:

```bash
# Create a draft
backlog draft create "Explore gamification of monthly challenges"

# List all drafts
backlog draft list --plain

# View a draft
backlog draft view 1

# Promote to a real task when ready
backlog draft promote 1

# Archive a draft that won't be pursued
backlog draft archive 1
```

---

## Task Lifecycle

```
DRAFT → TO DO → IN PROGRESS → DONE → [archive/completed]
  ↑                  ↓
  └── demote ←── (if work reveals it's not ready)
```

| Status | Meaning | Who sets it |
|--------|---------|-------------|
| `To Do` | Specified, ready to start | Anyone |
| `In Progress` | Actively being worked on | Assignee |
| `In Review` | Waiting for code review | Assignee |
| `Done` | Acceptance criteria all checked | Assignee |

### State transitions via CLI

```bash
backlog task edit N --status "In Progress"
backlog task edit N --status "In Review"
backlog task edit N --status "Done"
backlog task archive N          # move to completed/
backlog task demote N           # move back to drafts
```

---

## Working with Documents and Decisions

### Documents (specs, integration guides, reports)

```bash
# Create a document
backlog doc create "Idealist API Integration Guide" \
  --path docs/integrations/idealist.md

# List all documents
backlog doc list --plain

# View a document
backlog doc view idealist-api
```

### Architecture Decision Records (ADRs)

```bash
# Record a decision
backlog decision create "Use Alembic over Django migrations for schema management"

# ADR files appear in backlog/decisions/
```

ADR template (auto-created by `backlog decision create`):

```markdown
# Decision: [Title]

## Status: proposed | accepted | deprecated | superseded

## Context
[What situation forced this decision?]

## Decision
[What was decided?]

## Consequences
[What becomes easier? What becomes harder?]
```

---

## Kanban Board and Browser

```bash
# Terminal Kanban board
backlog board

# Horizontal layout (default)
backlog board --layout horizontal

# Group by milestone
backlog board --milestones

# Web browser UI (recommended for team reviews)
backlog browser
# Opens http://localhost:6420

# Export board to Markdown (for async stakeholder sharing)
backlog board export
backlog board export --filename "$(date +%Y-%m-%d)-sprint-review.md"
```

---

## Dependency Management

```bash
# Set dependency when creating
backlog task create "Add auth middleware" --dep 3 --dep 4

# Add dependency to existing task
backlog task edit 8 --dep 7

# View execution sequence (respects all dependencies)
backlog sequence list --plain

# Filter tasks without blockers
backlog task list --plain   # (check tasks whose deps are all Done)
```

**Dependency rules for MHS:**
- A task can only move to `In Progress` when all its `dependencies` are `Done`
- Never create circular dependencies
- Post-MVP tasks (900+) can depend on MVP tasks but not vice versa

---

## Task Templates

### Backend API Endpoint

```bash
backlog task create "GET /api/v1/scores/{user_id}" \
  --priority high \
  --labels "epic003-scoring,developer,sonnet" \
  --dep 7 \
  --ac "Returns MHS score breakdown for authenticated user" \
  --ac "Returns 404 if user not found" \
  --ac "Returns 403 if requesting another user's private data" \
  --ac "Response time < 200ms at p95" \
  --ac "OpenAPI schema updated"
```

### Frontend Component

```bash
backlog task create "ScoreRingChart component" \
  --priority medium \
  --labels "epic012-frontend,developer,sonnet,data-visualizer" \
  --dep 5 \
  --dep 8 \
  --ac "Renders 6-category radar chart using recharts" \
  --ac "Uses MHS_COLORS design tokens from design-tokens.ts" \
  --ac "Accessible: role=img, aria-label, sr-only figcaption" \
  --ac "Empty state renders when data=[]" \
  --ac "Storybook story added"
```

### Database Migration

```bash
backlog task create "Add indexes on activities table" \
  --priority high \
  --labels "epic001-foundation,developer,sonnet,database" \
  --dep 2 \
  --ac "alembic upgrade head completes in < 30s on 1M rows" \
  --ac "EXPLAIN ANALYZE shows index usage on common queries" \
  --ac "alembic downgrade -1 reverses cleanly"
```

### Data Quality Check

```bash
backlog task create "Weekly data quality report — activities table" \
  --priority medium \
  --labels "epic011-ml-ai,data-analyst,haiku" \
  --ac "Script runs in < 5 minutes on production DB size" \
  --ac "Report written to reports/quality/YYYY-MM-DD-activities.md" \
  --ac "Zero-tolerance violations cause non-zero exit code (CI fails)"
```

---

## MHS Label Conventions

Labels follow `category-slug` format. Use multiple labels per task.

### Epic labels (always include one)

| Label | Epic |
|-------|------|
| `epic001-foundation` | EPIC-001 Foundation & Infrastructure |
| `epic002-auth` | EPIC-002 Authentication & User Profiles |
| `epic003-scoring` | EPIC-003 MHS Scoring Engine |
| `epic004-activity` | EPIC-004 Activity System & Verification |
| `epic006-badges` | EPIC-006 Badge & Achievement System |
| `epic007-social` | EPIC-007 Social Feed & Timeline |
| `epic008-groups` | EPIC-008 Groups & Communities |
| `epic009-integrations` | EPIC-009 Platform Integrations |
| `epic010-admin` | EPIC-010 Admin & Governance |
| `epic011-ml-ai` | EPIC-011 ML/AI Services |
| `epic012-frontend` | EPIC-012 Frontend UI/UX |
| `epic990-angel-ai` | EPIC-990 Angel AI (post-MVP) |

### Agent / Role labels (always include one)

| Label | Role |
|-------|------|
| `developer` | Feature implementation |
| `tester` | QA, test suites |
| `data-analyst` | Data quality, labeling, MDM |
| `data-crawler` | Integrations, crawlers |
| `data-visualizer` | Charts, dashboards, widgets |
| `reviewer` | Code review, architecture |

### Model labels (always include one)

| Label | Model | Use for |
|-------|-------|---------|
| `sonnet` | claude-sonnet-4-6 | Complex features |
| `haiku` | claude-haiku-4-5 | Simple CRUD, tests |
| `opus` | claude-opus-4-7 | Architecture, analysis |
| `gemini-pro` | gemini-2.5-pro | Research, crawling |

### Special labels

| Label | Meaning |
|-------|---------|
| `post-mvp` | Not needed for MVP launch |
| `blocked` | Has an unresolved external blocker |
| `database` | Involves schema or migration changes |
| `security` | Security-sensitive change |
| `ethics` | Touches scoring algorithm or bias logic |
| `sprint-1` through `sprint-4` | Sprint assignment |

---

## AI Agent Integration

### MCP Server (recommended)

The Backlog.md MCP server lets Claude Code read and write tasks directly without CLI commands.

```bash
# Already configured — verify with:
claude mcp list   # should show: backlog ✓ Connected

# If you need to re-add:
claude mcp add backlog --scope user -- backlog mcp start
```

In Claude Code sessions, you can say:
> "Mark task 7 as In Progress"
> "Create a task for adding Redis caching to the scoring API"
> "What tasks are blocking task 19?"

### CCPM Skill (spec-driven delivery)

CCPM (`~/.claude/skills/ccpm`) enables PRD → Epic → GitHub Issues → Parallel Agents workflow.

```
In Claude Code, say:
  "Write a PRD for adding push notifications"
  "Parse this PRD into an epic"
  "Decompose the epic into tasks"
  "Sync tasks to GitHub Issues"
  "Start working on issue 7"
  "Run the standup"
```

### `backlog agents` — Sync instructions to AI tools

```bash
# Update CLAUDE.md, AGENTS.md, GEMINI.md with current backlog conventions
backlog agents --update-instructions
```
