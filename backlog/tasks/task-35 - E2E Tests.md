---
id: TASK-35
assignee: []
title: "E2E Tests"
status: To Do
priority: medium
labels: ["epic001-foundation-&-infrastructure", "haiku", "tester"]
dependencies:
  - task-5
  - task-6
acceptance_criteria:
  - "All 3 test scenarios pass in CI"
  - "Tests run against real running stack (not mocks)"
  - "Screenshots captured on failure"
  - "`npx playwright test` runs in < 2 minutes"
  - "Page Object Model used (no raw selectors in tests)"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-001 Foundation & Infrastructure
mhs_agent: Tester
mhs_model: claude-haiku-4-5
mhs_estimated_tokens: 20000
mhs_estimated_hours: 3
---

# TASK-035 — E2E Tests (Playwright)

## Description
End-to-end tests for critical user journeys using Playwright.
Runs against the full Docker Compose stack.

## Test scenarios

### Authentication flow
```
test("register and login")
  1. Navigate to /register
  2. Fill form (email, username, password)
  3. Submit → redirected to /feed or /u/{username}
  4. Profile page shows score = 0
  5. Log out → redirected to /login
  6. Log in with same credentials → profile accessible
```

### Profile viewing
```
test("view public profile")
  1. Navigate to /u/{username} (unauthenticated)
  2. MHS ring shows (score 0 for new user)
  3. "🌱 Awakening" level badge visible
  4. Empty badge grid shows onboarding CTA
```

### Protected route redirect
```
test("unauthenticated redirect")
  1. Navigate to /feed (not logged in)
  2. Redirected to /login
  3. Log in → redirected back to /feed
```

## Page Object Model
```
tests/e2e/
├── pages/
│   ├── LoginPage.ts
│   ├── RegisterPage.ts
│   └── ProfilePage.ts
├── auth.spec.ts
├── profile.spec.ts
└── playwright.config.ts
```

## CI integration
- Playwright tests run in CI after unit/integration tests pass
- Screenshots on failure (stored as CI artifacts)
- Headless Chromium only in CI (all browsers in local dev)

## Acceptance Criteria
- [ ] All 3 test scenarios pass in CI
- [ ] Tests run against real running stack (not mocks)
- [ ] Screenshots captured on failure
- [ ] `npx playwright test` runs in < 2 minutes
- [ ] Page Object Model used (no raw selectors in tests)
