---
name: mhs-verify-task
description: >
  Verify that a completed MHS / Kindora backlog task satisfies all its acceptance
  criteria. Use this skill whenever the user wants to check, verify, validate, or
  QA a task implementation ("did task-004 pass?", "verify the auth task", "check
  acceptance criteria for task-006", "is TASK-002 done?", "review what was built",
  "QA this task", "does it meet the spec?", "run acceptance checks"). Also triggers
  after a task is marked done and the user wants confirmation before moving on.
  This skill reads the task spec, runs relevant tests, checks each criterion
  systematically, and produces a clear pass/fail report. Use it proactively after
  any implementation session — don't just trust that it's done, verify it.
---

# MHS Task Acceptance Verification

You're verifying that an implemented feature meets its acceptance criteria
for the Kindora / My Humanity Score platform.

## Step 1 — Read the task spec

Find and read the task file:
- Given ID (e.g., "TASK-004") → `backlog/tasks/task-004-*.md`
- Given name → glob `backlog/tasks/` for matching filename

Extract all `- [ ]` acceptance criteria. These are your verification checklist.

Also note:
- `Dependencies:` — did those tasks complete first?
- `Agent:` / `Model:` — who was supposed to implement this?
- `Epic:` — for context on what "done" means

## Step 2 — Check that implementation exists

Before running tests, verify the expected files exist:

For backend tasks:
- Router file in `apps/api/routers/`
- Model file in `apps/api/models/`
- Migration in `alembic/versions/`
- Tests in `tests/unit/` and/or `tests/integration/`

For frontend tasks:
- Page file in `apps/web/app/`
- Component files in `apps/web/components/`
- Relevant type definitions

If files are missing, report immediately — don't proceed to run tests.

## Step 3 — Run the test suite

Always run tests first. They catch the most issues fastest.

```bash
# Backend tests
docker compose exec api pytest tests/ -v --tb=short 2>&1 | tail -50

# If task is test-heavy, run with coverage
docker compose exec api pytest tests/ --cov=apps/api --cov-report=term-missing

# Frontend tests
docker compose exec web npm run test -- --run
docker compose exec web npm run build  # Catches TypeScript errors
```

Report: how many passed, failed, and errored.

## Step 4 — Verify each acceptance criterion

Go through every `- [ ]` criterion in the task file. For each one:

### Category A — API / endpoint criteria
Check by making actual HTTP requests:
```bash
# Example patterns:
curl -s http://localhost:8000/health
curl -s -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"tester","password":"Test1234!"}'
```

### Category B — Security / data criteria
Things like "passwords never in response", "tokens encrypted in DB":
- Read the implementation code to verify
- Check that forbidden fields are absent from API response schemas (Pydantic models)
- For token encryption: check that `connected_platforms.access_token_encrypted` column
  name has `_encrypted` suffix and that the service encrypts before storing

### Category C — Ethics criteria (enforce strictly)
These are non-negotiable for any scoring task:
- Grep the implementation for `FORBIDDEN_SCORING_FEATURES` names:
  ```bash
  grep -r "religion\|ethnicity\|race\|gender\|sexual_orientation\|nationality" apps/api/services/
  ```
  If found in scoring logic → FAIL. No exceptions.
- Hidden factors: verify raw values never appear in Pydantic response schemas
  ```bash
  grep -r "carbon_penalty\|toxicity_index\|network_multiplier" apps/api/schemas/
  ```
  Should only appear as bucket strings ("low", "medium", "high")

### Category D — Database criteria
For migration tasks:
```bash
docker compose exec api alembic upgrade head    # Should succeed
docker compose exec api alembic downgrade -1    # Should reverse cleanly
docker compose exec postgres psql -U mhs -d mhs -c "\d users"  # Check columns
```

### Category E — Frontend criteria
- Visual checks: start dev server, navigate to the page
- TypeScript: `docker compose exec web npm run build` must pass
- Accessibility: note any obvious issues (missing aria-labels, color-only indicators)

### Category F — Performance criteria
If task specifies timing (e.g., "< 500ms"):
```bash
time curl -s http://localhost:8000/scores/testuser
```

## Step 5 — Produce verification report

Format your report as:

```
# Verification Report: TASK-XXX — [Task Title]

## Test Results
- Unit tests: X passed, Y failed
- Integration tests: X passed, Y failed
- Build: ✅ passing / ❌ failing

## Acceptance Criteria

✅ [Criterion 1] — verified by: <how you checked>
✅ [Criterion 2] — verified by: <how you checked>
⚠️ [Criterion 3] — PARTIAL: <what works, what doesn't>
❌ [Criterion 4] — FAIL: <what's wrong and why>
⏭️ [Criterion 5] — SKIPPED: requires live external API (Climatiq)

## Ethics Check
✅ No FORBIDDEN_SCORING_FEATURES in scoring logic
✅ Hidden factor raw values not exposed in API responses
[or ❌ with details]

## Summary
Status: PASS / PARTIAL / FAIL
Criteria: X/Y passing

[If PARTIAL or FAIL:]
## Required fixes
1. <specific fix needed>
2. <specific fix needed>
```

## Special verification rules by task type

### Auth tasks (TASK-004)
- Test the full register → login → refresh → logout flow with real requests
- Verify expired access token returns 401 (set expiry to 1 second in test config)
- Check no password appears in any log output or API response

### Score calculator tasks (TASK-007, TASK-008)
- Score of 0 for user with zero activities
- Score never < 0 or > 1000 (try extremes)
- All 7 level thresholds correct (0, 100, 250, 400, 550, 700, 850)
- Hidden factors never in API response — check Pydantic schema, not just runtime

### Frontend tasks (TASK-005, TASK-006, TASK-028–033)
- Run `npm run build` (TypeScript type check)
- If the page needs a running API, start the stack first
- Empty state renders correctly (new user with score = 0)
- Mobile viewport: check at 375px width

### ML/AI tasks (TASK-012–016)
- Mock external APIs in tests (Climatiq, HuggingFace) — no live calls in CI
- Known toxic string → correct threat level
- Known non-toxic string → NONE threat level
- Edge case: empty string, very long string, non-English text

### Database/migration tasks (TASK-002, schema changes)
- `alembic upgrade head` idempotent (run twice, no error second time)
- All foreign keys have `ON DELETE` behavior defined
- Indexes exist on filtered columns (check `\d+ tablename` in psql)

## If the task is PARTIAL or FAIL

Don't just report it — help fix it:
1. Identify the root cause of each failing criterion
2. Show the minimal code change needed
3. Re-run verification after applying fixes
4. Update the task file status accordingly:
   - All pass → `status: done`
   - Some fail → `status: in-review` (add notes about what failed)
