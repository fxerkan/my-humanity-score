You are setting up the My Humanity Score (MHS) project from scratch.
This is a PLAN MODE session — do NOT write any code yet.

## STEP 1: Read all context

Read these files in order:

1. `CLAUDE.md` — project context, tech stack, coding standards
2. `AGENTS.md` — agent roles and model routing
3. `.vibe/config.yml` — AI provider configuration
4. `concept/MHS_Custom_Instructions.md` — full platform spec
5. `concept/MHS_KB_01_Vision_Market.md` — vision and market research
6. `concept/MHS_KB_02_Technical.md` — technical architecture
7. `concept/MHS_KB_03_UX_Business_Ethics.md` — UX, badges, ethics

After reading, summarize what you understand about:

- What this platform does
- The scoring system (6 categories + hidden factors)
- The badge ecosystem (4 layers)
- The Angel AI system
- The ethics charter (no discrimination)

## STEP 2: Audit existing backlog

Read all files in `backlog/`:

- `backlog/epics/` — list all epics and their status
- `backlog/tasks/` — list all tasks with: id, title, status, agent, model

Output a table:
| ID | Title | Status | Agent | Model | Deps |

## STEP 3: Identify gaps

Based on the concept docs and the existing backlog, what important features
are NOT yet represented as tasks? List them.

Think specifically about:

- Missing API endpoints
- Missing frontend pages
- Missing ML/AI components
- Missing integrations
- Missing testing tasks

## STEP 4: Create missing tasks

For each gap identified in Step 3, create a task file at
`backlog/tasks/task-XXX-[name].md` using the standard format from
`.vibe/agents/analyst.md`.

## STEP 5: Create Sprint 1 plan

Create `backlog/sprints/sprint-01-foundation.md` containing:

```markdown
# Sprint 1 — Foundation
Duration: 2 weeks
Goal: Working dev environment + basic user profile with MHS display

## Tasks in this sprint (ordered)

### Sequential (must run one at a time)
- TASK-001: Repo setup + Docker + CI (Developer, Sonnet, ~3h)
- TASK-002: Database schema (Developer, Sonnet, ~2h)  [deps: 001]
- TASK-004: Authentication (Developer, Sonnet, ~4h)    [deps: 002, 003]
- TASK-006: User profile page (Developer, Sonnet, ~4h) [deps: 004, 005]

### Parallel (can run simultaneously)
- TASK-003: FastAPI structure (Developer, Sonnet) ← parallel with 002
- TASK-005: Next.js shell (Developer, Sonnet)     ← parallel with 003

## Definition of Done for Sprint 1
- [ ] docker compose up works
- [ ] User can register and see empty profile
- [ ] CI passes on GitHub
- [ ] No secrets committed

## Estimated tokens: ~165,000
## Recommended model: Sonnet (cost/quality balance)
```

## STEP 6: Output execution plan

Show the complete plan for how to execute Sprint 1 using Claude Code,
including exact commands to run for each task:

```
Sprint 1 Execution Plan:

Task 001 (Est: 3h, ~30K tokens):
  Command: claude "Read CLAUDE.md and backlog/tasks/task-001-repo-setup-docker-ci.md. 
            Read .vibe/agents/developer.md for your role. 
            Implement the full repository structure, Docker Compose dev environment,
            and GitHub Actions CI pipeline. Follow all acceptance criteria."
  Model: sonnet (default)
  
Task 002 + 003 (Parallel, Est: 2h each, ~45K tokens total):
  [Requires Agent Teams or 2 terminal windows]
  Terminal 1: claude "Read CLAUDE.md and backlog/tasks/task-002-*.md..."
  Terminal 2: claude "Read CLAUDE.md and backlog/tasks/task-003-*.md..."
  
[...continue for all tasks...]
```

## STEP 7: Model assignment review

Review all tasks in `backlog/tasks/` and flag any where the model assignment
could be optimized for cost. Apply the cost optimization rules from `AGENTS.md`.

Output: table of suggested model changes with rationale.

---

After completing all steps, output:

```
✅ Planning Complete
Epics: X
Features: X
Tasks: X (X ready to start, X blocked)
Sprint 1: X tasks (~X tokens, ~$X estimated)
Gaps found: X new tasks created
Model optimizations: X changes applied

Ready to start? Run:
  claude "Read .vibe/prompts/01-START-TASK-001.md"
```
