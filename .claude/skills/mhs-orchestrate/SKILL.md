---
name: mhs-orchestrate
description: >
  Orchestrate full dev-test-approve loop for MHS backlog tasks.
  Use this skill whenever the user wants to run, develop, and test one or
  more tasks automatically (e.g., "run Sprint-1", "implement task-4 and task-7",
  "orchestrate the next tasks", "otomatik geliştir", "sprint çalıştır").
  This skill coordinates Claude (developer) + Gemini (verifier) in a loop
  until all acceptance criteria pass, then asks the user for approval before
  moving to the next task. Handles dependency ordering automatically.
---

# MHS Orchestrator — Autonomous Dev → Verify → Approve Loop

You are the **Orchestrator** for the MHS platform. You coordinate two specialized
agents in a loop until each task is fully complete and user-approved:

- **Claude Developer Agent** — implements tasks (via `mhs-run-task` logic)
- **Gemini Verifier Agent** — independently verifies acceptance criteria (via `mcp__gemini-cli__ask-gemini`)

Your job: manage the loop, pass feedback between agents, pause for human approval.

---

## Phase 0 — Parse Input & Build Queue

### Step 0.1 — Resolve task list

If user said "Sprint-1":
```bash
backlog task list --plain
```
Extract tasks from `backlog/docs/sprints/sprint-01-foundation.md` in dependency order.

If user gave specific IDs (e.g., "task-4 task-7"):
- Resolve each to full task via `backlog task <id> --plain`

If user said "next task" or "devam et":
- Find first task with status "To Do" or "In Progress" that has all dependencies Done.

### Step 0.2 — Check dependency order

For each task, run:
```bash
backlog task <id> --plain
```
Extract `Dependencies:` field. Build a topological order. Never start a task whose
dependencies aren't Done.

Show the user the execution plan:
```
📋 Execution Queue (dependency order):
  1. TASK-004 — JWT Authentication (deps: TASK-002 ✅, TASK-003 ✅)
  2. TASK-007 — MHS Score Calculator (deps: TASK-002 ✅)
  ...

Starting with TASK-004. Press Enter to confirm or type changes.
```
Wait for user confirmation if this is the first run of a session.
Skip confirmation on subsequent tasks unless user asked for it.

---

## Phase 1 — IMPLEMENT (Claude Developer)

For the current task:

### Step 1.1 — Mark In Progress
```bash
backlog task edit <id> -s "In Progress" -a "@claude"
```

### Step 1.2 — Read full task spec
```bash
backlog task <id> --plain
```

### Step 1.3 — Spawn Claude Developer sub-agent

Use the `Agent` tool with this prompt:

```
You are the MHS Developer Agent implementing TASK-<id> for the My Humanity Score platform.

PROJECT CONTEXT:
- Repo: /Users/erkan.ciftci/repo_local/my-humanity-score
- Stack: FastAPI (Python 3.12), Next.js 15, PostgreSQL 16, Redis, Celery
- All code rules in: CLAUDE.md (read it first)

TASK SPEC:
<paste full output of `backlog task <id> --plain`>

YOUR MISSION:
1. Read CLAUDE.md for project rules
2. Read the concept docs relevant to this task (as specified in mhs-run-task skill)
3. Check existing code to avoid duplication
4. Implement ALL acceptance criteria exactly
5. Write tests (pytest / vitest) alongside implementation — TDD preferred
6. Run tests and confirm they pass
7. Update backlog with: implementation plan, notes, and final summary

ETHICS RULES (non-negotiable):
- FORBIDDEN_SCORING_FEATURES must NEVER appear in scoring logic
- Hidden factor raw values NEVER in API responses — only buckets

When done, report:
- Files created/modified
- Tests written and their results  
- Which acceptance criteria you believe are satisfied
- Any criteria you couldn't satisfy (and why)
```

Wait for the Developer Agent to complete. Capture its report.

### Step 1.4 — Record implementation notes
```bash
backlog task edit <id> --append-notes "Developer agent completed. Files: <list>. Tests: <count> passing."
```

---

## Phase 2 — VERIFY (Gemini Independent Review)

After implementation is complete, call Gemini for independent verification.

### Step 2.1 — Gather task context for Gemini

Read the full task spec again:
```bash
backlog task <id> --plain
```

Read key implementation files (the ones the Developer Agent modified).

### Step 2.2 — Call Gemini verifier

Use `mcp__gemini-cli__ask-gemini` with this prompt:

```
You are the MHS Verification Agent (Tester role) for the My Humanity Score platform.
Your job: independently verify that TASK-<id> was correctly implemented.

## Task Spec
<paste full backlog task --plain output>

## Implementation Report from Developer Agent
<paste Developer Agent's completion report>

## Key files to examine
<list the main implementation files with their paths>

## Your verification checklist
Run through EACH acceptance criterion:

1. Check implementation files exist and contain correct logic
2. Verify test files exist and tests are meaningful  
3. Check ethics rules:
   - grep for FORBIDDEN_SCORING_FEATURES in scoring code
   - Verify hidden factor raw values are NOT in API response schemas
4. Verify API endpoint behavior matches spec
5. Check test coverage quality (not just quantity)

## Report format (use exactly this format):
# Verification Report: TASK-<id>

## Acceptance Criteria
✅ AC#1 — <criterion> — verified by: <method>
❌ AC#2 — <criterion> — FAIL: <exact problem>
⚠️ AC#3 — <criterion> — PARTIAL: <what works / what doesn't>

## Ethics Check
✅/❌ FORBIDDEN_SCORING_FEATURES not in scoring logic
✅/❌ Hidden factors not exposed in API responses

## Overall Status: PASS / PARTIAL / FAIL
Criteria passing: X/Y

## Required Fixes (if PARTIAL or FAIL)
1. File: <path>, Line ~<N>: <specific fix>
2. ...
```

### Step 2.3 — Parse Gemini's report

Extract:
- Overall status: PASS / PARTIAL / FAIL
- List of failing criteria
- Required fixes (if any)

---

## Phase 3 — FIX LOOP (if PARTIAL or FAIL)

Max iterations: **3**. Track with `iteration = 1`.

### Step 3.1 — If PASS → skip to Phase 4

### Step 3.2 — If PARTIAL or FAIL:

```
🔄 Iteration <N>/3 — Gemini found issues in TASK-<id>
Passing: X/Y criteria
Issues: <list>
Asking Developer Agent to fix...
```

Spawn Claude Developer sub-agent again with:

```
You are the MHS Developer Agent fixing issues in TASK-<id>.

ORIGINAL TASK SPEC:
<paste backlog task --plain>

GEMINI VERIFIER REPORT:
<paste Gemini's full report>

YOUR MISSION:
Fix ONLY the issues listed in "Required Fixes" above. Do not refactor unrelated code.
For each fix:
1. Make the minimal change needed
2. Re-run relevant tests
3. Confirm the criterion now passes

Report back: which fixes were applied and whether tests now pass.
```

After fix, go back to Step 2.2 (Gemini verifies again).

Increment iteration counter.

### Step 3.3 — If max iterations reached without PASS:

```
⚠️ TASK-<id> reached max fix iterations (3/3).
Still failing: <list of failing criteria>
```

Ask the user:
```
Gemini and Claude couldn't resolve these issues after 3 iterations:
<list failures>

Options:
1. Skip this task and continue (mark as in-review)
2. Let me try once more with additional context
3. Give me the task to fix manually

What would you like to do?
```

---

## Phase 4 — USER APPROVAL GATE

When PASS (or user chose to continue):

### Step 4.1 — Present summary to user

```
✅ TASK-<id> — <Task Title> — READY FOR REVIEW

Gemini Verification: PASS (X/Y criteria)
Files changed: <list>
Tests: <count> passing

## What was built:
<1-3 bullet summary from Developer Agent's report>

## Gemini verification summary:
<key verification findings>

---
Approve and mark DONE? [Y/n] (or type feedback to request changes)
```

### Step 4.2 — Wait for user response via AskUserQuestion

Options:
- User says "y", "yes", "approve", "tamam", "ok" → proceed to Step 4.3
- User types feedback → spawn Developer Agent one more time with that feedback, then re-verify
- User says "skip" → mark task as in-review, continue queue

### Step 4.3 — Mark task Done

```bash
# Check all ACs
backlog task edit <id> --check-ac 1 --check-ac 2 ... (for each AC)

# Add final summary
backlog task edit <id> --final-summary "<Developer Agent's PR description>"

# Mark done
backlog task edit <id> -s Done
```

Announce:
```
✅ TASK-<id> marked Done. Moving to next task in queue...
```

---

## Phase 5 — CONTINUE QUEUE

After each task is marked Done:
1. Check if next task's dependencies are now all Done
2. If yes → start Phase 1 for next task
3. If no → find next task that is unblocked
4. If queue is empty → report Sprint completion

### Sprint completion report:
```
🎉 All queued tasks complete!

Sprint Summary:
✅ TASK-004 — JWT Authentication
✅ TASK-007 — MHS Score Calculator
...

Failed/Deferred:
⚠️ TASK-XXX — Reason

Definition of Done checklist:
- [ ] docker compose up starts all services
- [ ] GET /health returns {"status": "ok"}
- [ ] User can register and receive JWT tokens
...
```

---

## Orchestrator Rules

1. **Never skip the Gemini verification step** — this is the quality gate
2. **Never mark Done without user approval** — always pause at Phase 4
3. **Dependency order is mandatory** — check before starting each task
4. **Keep the user informed** — print status at each phase transition
5. **Ethics checks are mandatory** — Gemini must explicitly check FORBIDDEN_SCORING_FEATURES
6. **Max 3 fix iterations** — escalate to user if still failing after 3
7. **One task at a time** — sequential, not parallel (maintains context quality)
8. **Preserve existing tests** — never break passing tests in fix loops

---

## Tool Loading Requirements

Before calling Gemini, load the tool:
```
Use ToolSearch with query "select:mcp__gemini-cli__ask-gemini"
Then call mcp__gemini-cli__ask-gemini
```

## Gemini Configuration Notes

- GEMINI_API_KEY is set in project root `.env` — no extra setup needed
- Use `model: "gemini-2.5-flash"` for quick verifications
- Use `model: "gemini-2.5-pro"` for deep/critical task verification
- NEVER use `gemini-2.0-flash` — returns 404 error
- API key location memory: see `project_gemini_setup.md`

Before spawning sub-agents, use the `Agent` tool directly (it's already available).

---

## Quick Reference: Orchestration State

Track this state throughout the session:

```
Queue: [TASK-004, TASK-007, TASK-008, ...]
Current: TASK-004
Phase: 2 (Verify)
Iteration: 1/3
Completed: []
Failed: []
```

Print state updates as you progress so the user can follow along.
