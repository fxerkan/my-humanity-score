---
id: TASK-4
assignee: []
title: "JWT Authentication + Refresh Tokens"
status: To Do
priority: high
labels: ["epic002-authentication-&-user-profiles", "sonnet", "developer"]
dependencies:
  - task-2
  - task-3
acceptance_criteria:
  - "Register creates user + mhs_scores row atomically"
  - "Login fails with generic \"invalid credentials\" (no email enumeration)"
  - "Refresh token rotation invalidates old token immediately"
  - "Expired access token returns HTTP 401"
  - "Used refresh token returns HTTP 401 (replay protection)"
  - "`get_current_user` dependency works on all protected routes"
  - "Passwords never logged or returned in any response"
  - "Integration tests cover: register → login → refresh → logout flow"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-002 Authentication & User Profiles
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 35000
mhs_estimated_hours: 4
---

# TASK-004 — JWT Authentication + Refresh Tokens

## Description
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

## Acceptance Criteria
- [ ] Register creates user + mhs_scores row atomically
- [ ] Login fails with generic "invalid credentials" (no email enumeration)
- [ ] Refresh token rotation invalidates old token immediately
- [ ] Expired access token returns HTTP 401
- [ ] Used refresh token returns HTTP 401 (replay protection)
- [ ] `get_current_user` dependency works on all protected routes
- [ ] Passwords never logged or returned in any response
- [ ] Integration tests cover: register → login → refresh → logout flow
