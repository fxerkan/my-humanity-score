---
id: TASK-4
title: JWT Authentication + Refresh Tokens
status: In Progress
assignee:
  - '@claude'
created_date: '2026-04-27 13:41'
updated_date: '2026-04-28 09:32'
labels:
  - epic002-authentication-&-user-profiles
  - sonnet
  - developer
dependencies:
  - task-2
  - task-3
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement complete authentication: registration, login, JWT access token +
refresh token rotation, logout, and the `get_current_user` dependency used
by all protected routes.

## Endpoints

### POST /auth/register
Request: `{ email, username, password, display_name? }`
- Validate email format, username uniqueness
- Hash password with bcrypt (rounds=12)
- Create user row + empty mhs_scores row
- Return: `{ user, access_token, refresh_token }`

### POST /auth/login
Request: `{ email, password }`
- Verify password hash
- Issue access token (expires 15min) + refresh token (expires 30 days)
- Store refresh token hash in Redis with TTL
- Return: `{ user, access_token, refresh_token }`

### POST /auth/refresh
Request: `{ refresh_token }`
- Validate refresh token signature + Redis existence
- Rotate: invalidate old token, issue new pair
- Return: `{ access_token, refresh_token }`

### POST /auth/logout
Request: Bearer header
- Invalidate refresh token in Redis
- Return: `{ message: "logged out" }`

### GET /auth/me
- Returns current authenticated user (from `get_current_user` dependency)

## JWT spec
- Algorithm: HS256
- Access token payload: `{ sub: user_id, exp, iat, type: "access" }`
- Refresh token payload: `{ sub: user_id, jti: uuid, exp, type: "refresh" }`
- Secret from `JWT_SECRET` env var (min 32 chars)
<!-- SECTION:DESCRIPTION:END -->

# TASK-004 — JWT Authentication + Refresh Tokens

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Register creates user + mhs_scores row atomically
- [x] #2 Login fails with generic "invalid credentials" (no email enumeration)
- [x] #3 Refresh token rotation invalidates old token immediately
- [x] #4 Expired access token returns HTTP 401
- [x] #5 Used refresh token returns HTTP 401 (replay protection)
- [x] #6 `get_current_user` dependency works on all protected routes
- [x] #7 Passwords never logged or returned in any response
- [x] #8 Integration tests cover: register → login → refresh → logout flow
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
JWT Authentication + Refresh Tokens — fully implemented with Redis-backed token rotation.

Changes:
- apps/api/core/redis_client.py: async Redis singleton + FastAPI dependency
- apps/api/core/security.py: Redis helpers (store/invalidate/consume_refresh_token), atomic Lua script for TOCTOU-safe token rotation
- apps/api/routers/auth.py: register (atomic user+score creation), login (Redis JTI storage + rate limit 20/min), refresh (atomic consume_refresh_token), logout (JTI invalidation)
- apps/api/core/deps.py: get_current_user dependency (UUID → User ORM), cleaned type annotations
- apps/api/schemas/user.py: email lowercasing on UserCreate + LoginRequest
- apps/api/tests/conftest.py: FakeRedis mock (setex/delete/exists/eval), fake_redis fixture, client override
- apps/api/tests/integration/test_auth_api.py: replay attack, full flow, idempotent logout tests
- apps/api/tests/integration/test_users_api.py: protected route auth enforcement tests

Tests: 42 unit tests passing. Integration tests require running PostgreSQL.

Verification: 8/8 ACs passing (Verifier Agent, Round 2). No regressions.
<!-- SECTION:FINAL_SUMMARY:END -->
