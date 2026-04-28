# Gemini Verifier Prompt Templates

## When to use Gemini vs Claude for verification

Use Gemini for independent verification because:
- Different model = different blind spots
- Catches things Claude might miss (Claude wrote the code, may rationalize)
- Provides adversarial review perspective

## Gemini call pattern

```
Tool: mcp__gemini-cli__ask-gemini
Model: gemini-2.0-flash (default) or gemini-2.5-pro for complex tasks
```

## Prompt structure for verification

```
ROLE: You are an independent QA verifier for the My Humanity Score (MHS) open-source platform.

CONTEXT:
- MHS is a platform measuring positive human impact (score 0-1000)
- Stack: FastAPI + PostgreSQL + Next.js 15
- Ethics rules: FORBIDDEN_SCORING_FEATURES (religion, ethnicity, race, gender, 
  sexual_orientation, nationality, language, disability, political_affiliation, 
  economic_status) must NEVER appear in scoring logic
- Hidden adjustment factors must NEVER be exposed as raw values in API responses

TASK SPEC:
[TASK ID + full backlog output]

IMPLEMENTATION REPORT:
[Developer agent's report]

FILES TO REVIEW:
[List with content of key changed files]

VERIFY EACH CRITERION:
[List of acceptance criteria]

OUTPUT FORMAT:
Use exactly this format:
# Verification Report: TASK-<id>
## Acceptance Criteria
✅/❌/⚠️ AC#N — text — verified by: method OR FAIL: reason
## Ethics Check  
✅/❌ result
## Overall Status: PASS / PARTIAL / FAIL
## Required Fixes (numbered list if needed)
```

## Tips for effective Gemini prompts

1. **Include actual file contents** — don't just say "check the file", paste the code
2. **Be specific about what to check** — list each AC explicitly
3. **Ask for specific fix locations** — "File X, function Y, line ~N"
4. **Request binary verdicts** — PASS or FAIL, not "looks good but..."
5. **Limit to 10 files max** — focus Gemini on what matters most

## Gemini response parsing

Extract from Gemini's response:
- Lines starting with `✅` = passing
- Lines starting with `❌` = failing (collect these)
- Lines starting with `⚠️` = partial (collect these)  
- "Overall Status:" line = PASS / PARTIAL / FAIL
- "Required Fixes:" section = what to tell Claude to fix

## Escalation criteria

Escalate to user (don't auto-fix) when Gemini reports:
- Ethics violation (FORBIDDEN_SCORING_FEATURES in scoring)
- Security issue (secrets in code, SQL injection, etc.)
- Breaking change to existing API contracts
- Missing database migration for schema change
