---
id: TASK-34
milestone: "M5: Pre-MVP Demo"
assignee: []
title: "Unit + Integration Test Suite"
status: To Do
priority: high
labels: ["epic001-foundation-&-infrastructure", "haiku", "tester"]
dependencies:
  - task-1
  - task-10
acceptance_criteria:
  - "`pytest` passes with no failures"
  - "Coverage report generated: `pytest --cov=apps/api`"
  - "Integration tests use real DB (no SQLite, no mocks)"
  - "Each test is independent (no shared state between tests)"
  - "Tests run in < 60 seconds total"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-001 Foundation & Infrastructure
mhs_agent: Tester
mhs_model: claude-haiku-4-5
mhs_estimated_tokens: 25000
mhs_estimated_hours: 3
---

# TASK-034 — Unit + Integration Test Suite

## Description
Comprehensive test suite for Sprint 1 backend code: unit tests for
score calculator and integration tests for auth/API endpoints.

## Unit tests (pytest)

### Score calculator (`tests/unit/test_mhs_calculator.py`)
- Zero score for user with no activities
- Score calculation with all 6 categories populated
- Carbon penalty at each threshold (0, 1000, 5000, 10000 kg)
- Toxicity penalty at 0.0, 0.5, 0.85, 1.0
- Network multiplier at 1.0 and 1.5 (capped)
- Score never < 0 or > 1000 (fuzz test with random inputs)
- Correct level assigned for each of 7 ranges

### Auth flows (`tests/unit/test_auth.py`)
- Password hashing and verification
- JWT token generation + validation
- Refresh token rotation
- Expired token rejection

## Integration tests (pytest + real PostgreSQL)
These hit the actual database — no mocks.

### Auth API (`tests/integration/test_auth_api.py`)
- Register → verify user created in DB
- Login → receive valid JWT
- Refresh → old token invalidated, new pair issued
- Logout → token rejected on next use
- Login with wrong password → 401 (not 404)

### User API (`tests/integration/test_users_api.py`)
- Create user → GET profile returns data
- Unauthenticated GET public profile → 200
- Unauthenticated GET private profile → 404

## Test configuration
```python
# conftest.py
@pytest.fixture
def test_db():
    # Use separate test database: mhs_test
    # Run migrations before each test session
    # Rollback after each test (no state leakage)
```

## Coverage target
- Score calculator: 100%
- Auth service: 90%+
- User endpoints: 85%+
- Overall: 80%+

## Acceptance Criteria
- [ ] `pytest` passes with no failures
- [ ] Coverage report generated: `pytest --cov=apps/api`
- [ ] Integration tests use real DB (no SQLite, no mocks)
- [ ] Each test is independent (no shared state between tests)
- [ ] Tests run in < 60 seconds total
