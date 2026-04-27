---
id: TASK-23
assignee: []
title: "Group System Backend"
status: To Do
priority: medium
labels: ["epic008-groups-&-communities", "sonnet", "developer"]
dependencies:
  - task-4
acceptance_criteria:
  - "Open group join is immediate"
  - "Closed group creates pending request"
  - "Only admin can approve requests"
  - "Group member count updates atomically with joins/leaves"
  - "User can only be in a group once (enforced by primary key)"
  - "Group feed only shows activities of current members"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-008 Groups & Communities
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 35000
mhs_estimated_hours: 4
---

# TASK-023 — Group System Backend

## Description
Full group CRUD with member management, join flow, and group roles.
Groups can be open (anyone joins) or closed (admin approves joins).

## Group types
- `open`: Anyone can join immediately
- `closed`: Join requests require admin approval
- `thematic`: Topic-based (e.g., "Climate Warriors")
- `local`: Location-based (e.g., "Istanbul Volunteers")
- `corporate`: Company-affiliated (invite-only)

## Endpoints

### POST /groups
Create group. Creator becomes admin.

### GET /groups?type=&location=&theme=&page=
Browse/search groups.

### GET /groups/{id}
Group details: info, stats, member preview, recent activity.

### POST /groups/{id}/join
- Open group: immediate join
- Closed group: creates join request

### POST /groups/{id}/requests/{request_id}/approve
Admin-only: approve join request.

### DELETE /groups/{id}/members/{user_id}
Remove member (admin) or leave (self).

### GET /groups/{id}/members?page=
List members with their individual MHS scores.

### GET /groups/{id}/feed?page=
Group activity feed (member activities tagged to group).

## Member roles
- `admin`: can edit group, approve joins, remove members
- `member`: standard access

## Database additions
```sql
CREATE TABLE group_members (
  group_id UUID REFERENCES groups(id),
  user_id UUID REFERENCES users(id),
  role VARCHAR(20) DEFAULT 'member',
  joined_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (group_id, user_id)
);

CREATE TABLE group_join_requests (
  id UUID PRIMARY KEY,
  group_id UUID REFERENCES groups(id),
  user_id UUID REFERENCES users(id),
  status VARCHAR(20) DEFAULT 'pending',
  requested_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Acceptance Criteria
- [ ] Open group join is immediate
- [ ] Closed group creates pending request
- [ ] Only admin can approve requests
- [ ] Group member count updates atomically with joins/leaves
- [ ] User can only be in a group once (enforced by primary key)
- [ ] Group feed only shows activities of current members
