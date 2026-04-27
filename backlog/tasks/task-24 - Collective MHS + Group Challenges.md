---
id: TASK-24
assignee: []
title: "Collective MHS + Group Challenges"
status: To Do
priority: medium
labels: ["epic008-groups-&-communities", "sonnet", "developer"]
dependencies:
  - task-23
  - task-7
acceptance_criteria:
  - "Collective MHS updates within 1 minute of member score change"
  - "Collective MHS formula applies weighted average correctly"
  - "Challenge progress increments on matching verified activity"
  - "Completed challenge awards group badge to all members"
  - "Challenge end date triggers auto-close even if not completed"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-008 Groups & Communities
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 30000
mhs_estimated_hours: 3
---

# TASK-024 — Collective MHS + Group Challenges

## Description
Aggregate individual MHS scores into a group collective score,
and implement the group challenge system with progress tracking.

## Collective MHS
```python
def collective_mhs(group_id: str) -> float:
    scores = [member.mhs_score for member in group.members]
    if not scores: return 0.0
    # Weighted average: top 20% count 40%, rest 60%
    # Capped at 1000 regardless of member count
    sorted_scores = sorted(scores, reverse=True)
    top_n = max(1, len(sorted_scores) // 5)
    top_avg = mean(sorted_scores[:top_n])
    rest_avg = mean(sorted_scores[top_n:]) if sorted_scores[top_n:] else 0
    return min(1000, top_avg * 0.4 + rest_avg * 0.6)
```

## Group challenges
Example: "May Green Month — Plant 100 trees by May 31"

### Challenge schema
```sql
CREATE TABLE group_challenges (
  id UUID PRIMARY KEY,
  group_id UUID REFERENCES groups(id),
  title VARCHAR(200) NOT NULL,
  description TEXT,
  activity_type VARCHAR(50),      -- linked to activity category
  target_count INTEGER,            -- e.g., 100 trees
  current_count INTEGER DEFAULT 0,
  start_date DATE,
  end_date DATE,
  status VARCHAR(20) DEFAULT 'active',
  badge_reward VARCHAR(50)
);
```

### Progress tracking
- When a member submits a verified activity matching the challenge type,
  increment `current_count`
- Auto-complete challenge when `current_count >= target_count`
- Award group Layer 4 badge to all members on completion

### Endpoints
```
POST /groups/{id}/challenges        # Create challenge (admin only)
GET  /groups/{id}/challenges        # List challenges
GET  /groups/{id}/challenges/{cid}  # Challenge detail with leaderboard
```

## Acceptance Criteria
- [ ] Collective MHS updates within 1 minute of member score change
- [ ] Collective MHS formula applies weighted average correctly
- [ ] Challenge progress increments on matching verified activity
- [ ] Completed challenge awards group badge to all members
- [ ] Challenge end date triggers auto-close even if not completed
