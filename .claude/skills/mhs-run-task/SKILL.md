---
name: mhs-run-task
description: >
  Execute a My Humanity Score (MHS) backlog task end-to-end in the My Humanity Score (MHS) project.
  Use this skill whenever the user mentions running, starting, implementing, or working
  on a specific task (e.g., "run TASK-001", "implement task-004", "work on the auth task",
  "start the database schema task"). Also triggers when the user says "next task", "pick
  up where we left off", or wants to execute anything from backlog/tasks/. This skill
  loads the task spec, selects the correct agent role and model, implements the full
  feature with tests, and marks the task done. Always use this skill rather than
  improvising — the task files contain acceptance criteria that must be checked.
---

# MHS Task Execution

You're implementing a feature for the MHS /  My Humanity Score platform.
This is a 100% free, open-source platform measuring positive human impact.
Every task has a spec file with acceptance criteria you must satisfy.

## Step 1 — Locate the task

If the user gave a task ID (e.g., "TASK-004" or "task-004"), the file is:
`backlog/tasks/task-004-<slug>.md`

If they said "next task" or didn't specify, find the first task with `status: ready`
in `backlog/tasks/` by reading each task file's metadata block.

Read the full task file now. Do not proceed until you've read it.

## Step 2 — Load your agent role

Check the task's `Agent:` field and read the corresponding role file:
- Developer → `.vibe/agents/developer.md`
- Tester → `.vibe/agents/tester.md`
- Analyst → `.vibe/agents/analyst.md`
- Reviewer → `.vibe/agents/reviewer.md`
- Researcher → `.vibe/agents/researcher.md`

If the `.vibe/agents/` files don't exist yet, use the role description from `AGENTS.md`.

Also check the `Model:` field. If it says Haiku, remind the user to pass
`--model claude-haiku-4-5-20251001` for cost savings.

## Step 3 — Read required context

Before touching any code, read these based on what the task touches:

| Task involves | Read first |
|---|---|
| Any scoring logic | `concept/MHS_KB_02_Technical.md` (MHSCalculator class) |
| Badges or UX | `concept/MHS_KB_03_UX_Business_Ethics.md` |
| Angel AI | `concept/MHS_KB_03_UX_Business_Ethics.md` (Angel AI spec) |
| Activities or verification | `concept/MHS_KB_02_Technical.md` (verification pipeline) |
| Platform vision / new feature | `concept/MHS_KB_01_Vision_Market.md` |
| Infrastructure, DB, FastAPI | Check for existing code in `apps/api/` first |
| Frontend | Check for existing code in `apps/web/` first |

Never skip this step for scoring, badge, or Angel AI tasks — the spec details matter.

## Step 4 — Check existing code

Before writing anything new, look for code that already exists:
- Scan the relevant `apps/` subdirectory for related files
- Check if migrations, models, or components partially exist
- Avoid duplicating code that's already there

## Step 5 — Implement

Follow the task spec exactly. Key project-wide rules:

**Ethics (never negotiate these):**
- FORBIDDEN_SCORING_FEATURES must never appear in scoring logic:
  `religion, ethnicity, race, gender, sexual_orientation, nationality,
  language, disability, political_affiliation, economic_status`
- Hidden factor raw values (carbon kg, toxicity index) must never appear
  in API responses — only buckets ("low", "medium", "high")

**Code quality:**
- Python: type hints on all functions, Pydantic v2 models, Google-style docstrings,
  Black + Ruff formatting. Max 50 lines per function.
- TypeScript: strict mode, no `any`, Zod for runtime validation
- No hardcoded secrets — always use environment variables from `.env.example`

**Tests:**
- Write tests alongside the implementation (TDD preferred)
- Integration tests must use a real database — no SQLite mocks
- Coverage target: 80% minimum on new code
- pytest for Python, vitest for TypeScript

**Alembic:**
- Any schema change needs a migration: `alembic revision --autogenerate -m "description"`
- Test that `alembic upgrade head` and `alembic downgrade -1` both work

## Step 6 — Verify acceptance criteria

After implementation, go through each `- [ ]` checkbox in the task file one by one.
For each criterion:
- If it's testable by running code, run it
- If it's a structural check (file exists, no secrets), verify it
- If it requires a running service, note it clearly

Report which criteria pass ✅ and which need attention ⚠️.

## Step 7 — Update task status

Change the task file's `status:` field from `ready` → `done` (or `in-review`
if it needs human review before closing).

Add a completion note at the bottom of the task file:
```
## Completion Notes
- Completed: <date>
- Files changed: <list>
- Tests added: <count>
- Notes: <anything surprising or deferred>
```

## Common patterns in this codebase

**FastAPI endpoint pattern:**
```python
@router.get("/{username}", response_model=UserPublicResponse)
async def get_user_profile(
    username: str,
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
) -> UserPublicResponse:
    ...
```

**Next.js page pattern (App Router):**
```typescript
export default async function ProfilePage({
  params,
}: {
  params: { username: string }
}) {
  // Server component — fetch directly, no useEffect
}
```

**Celery task pattern:**
```python
@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def recalculate_score(self, user_id: str) -> None:
    ...
```

## If you get blocked

- Missing dependency → add to requirements.txt or package.json, note in completion notes
- Ambiguous spec → implement the most reasonable interpretation and note the decision
- External API not available → mock it with a stub and mark the criterion as "needs live API"
- Existing code conflicts → do not break existing tests; add a note explaining the conflict
