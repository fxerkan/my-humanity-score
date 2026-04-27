# Ethics Verification Checklist

This applies to every task that touches scoring, badges, or user data.

## Discrimination prevention (CRITICAL — always check)

```bash
# These must NEVER appear in scoring functions or models:
FORBIDDEN = [
    "religion", "ethnicity", "race", "gender", "sexual_orientation",
    "nationality", "language", "disability", "political_affiliation",
    "economic_status", "education_level"
]

# Search command:
grep -rn "religion\|ethnicity\|race\|gender\|sexual_orientation\|nationality\|language\|disability\|political_affiliation\|economic_status" \
  apps/api/services/ apps/api/models/ packages/score-engine/
```

If any of these appear in scoring logic → **IMMEDIATE FAIL**. No exceptions, no workarounds.

They CAN appear in:
- User profile fields (users choose to share optionally)
- `BiasAuditor` class (checking for bias)
- GDPR export (returning user's own data)
- `FORBIDDEN_SCORING_FEATURES` constant definition

They CANNOT appear in:
- `MHSCalculator` or any score calculation
- Activity verification logic
- Badge award criteria
- Leaderboard filtering

## Hidden factor exposure (CRITICAL)

Hidden factors (carbon_penalty, toxicity_penalty, network_multiplier, etc.)
must NEVER be exposed as raw numbers in API responses.

**Allowed in responses:**
```python
"carbon_bucket": "low"       # ✅ OK
"toxicity_status": "clean"   # ✅ OK
"network_effect": "positive" # ✅ OK
```

**Never in responses:**
```python
"carbon_penalty": -40        # ❌ FORBIDDEN
"toxicity_index": 0.73       # ❌ FORBIDDEN
"network_multiplier": 1.23   # ❌ FORBIDDEN
```

Check Pydantic response schemas — if the field is in the schema, it will appear in the response.

## Data privacy

- Access tokens in `connected_platforms` must use `_encrypted` suffix and actually be AES-256 encrypted
- User passwords must be bcrypt hashed — never stored plain
- PII (email, location) must be excluded from leaderboard and public feed responses
- Deleted users: soft delete first (`deleted_at`), hard anonymize after 30 days

## Open source compliance

- No proprietary dependencies (check license of any new package)
- AGPL-3.0: any modification must be open-sourced (this is intentional)
- No telemetry or tracking code
