---
id: TASK-35
title: E2E Tests
status: In Progress
assignee:
  - '@developer'
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 17:08'
labels:
  - epic001-foundation-&-infrastructure
  - haiku
  - tester
dependencies:
  - task-5
  - task-6
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
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
<!-- SECTION:DESCRIPTION:END -->

# TASK-035 — E2E Tests (Playwright)

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 All 3 test scenarios pass in CI
- [x] #2 Tests run against real running stack (not mocks)
- [x] #3 Screenshots captured on failure
- [x] #4 `npx playwright test` runs in < 2 minutes
- [x] #5 Page Object Model used (no raw selectors in tests)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Install Playwright + @playwright/test in apps/web
2. Create playwright.config.ts pointing at localhost:3000
3. Create Page Object Model: LoginPage, RegisterPage, ProfilePage
4. Create auth.spec.ts, profile.spec.ts with the 3 test scenarios
5. Update package.json scripts
6. Note: AC#1 (all 3 pass) depends on TASK-005/006 UI pages; scaffold passes when stack is up
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
AC#1 (all 3 scenarios pass): infra ready, tests will fully pass once TASK-005 (Next.js App Shell) and TASK-006 (User Profile Page) deliver /register, /login, /feed, and /u/{username} pages.

❌ QA NOTE (Gemini): AC#1 not yet verifiable — UI pages (/register, /login, /u/{username}) require TASK-005 + TASK-006. Infrastructure (Playwright config, page objects, spec files, CI job) is fully implemented and reviewed PASS. Status kept In Progress until UI tasks deliver the pages.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Playwright E2E test infrastructure fully scaffolded.

Files created:
- apps/web/tests/e2e/playwright.config.ts: headless Chromium in CI, all 3 browsers locally; screenshots+video on failure; 30s test timeout
- apps/web/tests/e2e/pages/LoginPage.ts: POM for /login (email, password, submit, error)
- apps/web/tests/e2e/pages/RegisterPage.ts: POM for /register (email, username, password, submit)
- apps/web/tests/e2e/pages/ProfilePage.ts: POM for /u/{username} (score ring, level badge, badge grid, onboarding CTA, logout)
- apps/web/tests/e2e/auth.spec.ts: register→profile→logout→login flow + unauthenticated redirect scenario
- apps/web/tests/e2e/profile.spec.ts: public profile view (score ring, Awakening level, onboarding CTA)

Updated:
- apps/web/package.json: added test:e2e, test:e2e:ui, test:e2e:all scripts
- .github/workflows/ci.yml: added e2e job (runs after api+web jobs, starts full Docker stack, uploads report+screenshots as artifacts)

Note: AC#1 (all 3 scenarios pass end-to-end) will be fully verified once TASK-005 + TASK-006 deliver the UI pages.
<!-- SECTION:FINAL_SUMMARY:END -->
