---
id: TASK-20
assignee: []
title: "Celery + Redis Background Jobs"
status: To Do
priority: high
labels: ["epic001-foundation-&-infrastructure", "sonnet", "developer"]
dependencies:
  - task-3
acceptance_criteria:
  - "Celery worker starts in Docker Compose"
  - "Celery Beat scheduler runs periodic tasks at correct times"
  - "`recalculate_score` runs after each activity verification"
  - "Failed tasks retry 3 times with exponential backoff"
  - "Task results retrievable by task_id for polling"
  - "Dead-letter queue for tasks that fail all retries"
  - "Celery Flower monitoring available at `localhost:5555` in dev"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-001 Foundation & Infrastructure
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 25000
mhs_estimated_hours: 3
---

# TASK-020 — Celery + Redis Background Jobs

## Description
Configure Celery with Redis as broker and result backend.
Define all background tasks used across the platform.

## Celery configuration
```python
# apps/api/celery_app.py
app = Celery(
    "mhs",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["tasks.scoring", "tasks.verification", "tasks.sync", "tasks.angel_ai"],
)
app.conf.beat_schedule = {
    "weekly-carbon-update": {
        "task": "tasks.scoring.update_carbon_scores",
        "schedule": crontab(day_of_week=1, hour=2),  # Monday 02:00
    },
    "monthly-mentor-summaries": {
        "task": "tasks.angel_ai.generate_monthly_summaries",
        "schedule": crontab(day_of_month=1, hour=6),  # 1st of month 06:00
    },
    "daily-score-recalculation": {
        "task": "tasks.scoring.recalculate_stale_scores",
        "schedule": crontab(hour=3),  # 03:00 daily
    },
}
```

## Background tasks to define

### tasks/scoring.py
- `recalculate_score(user_id)` — triggered after activity verified
- `recalculate_stale_scores()` — daily batch for stale scores
- `update_carbon_scores()` — weekly Climatiq refresh

### tasks/verification.py
- `verify_activity(activity_id)` — runs 5-layer pipeline
- `send_org_email(activity_id)` — layer 4 email

### tasks/sync.py
- `sync_github(user_id)` — import GitHub contributions
- `sync_linkedin(user_id)` — import LinkedIn volunteer data

### tasks/angel_ai.py
- `generate_monthly_summaries()` — batch Mentor summaries
- `guardian_analyze(content, user_id)` — async Guardian check

## Acceptance Criteria
- [ ] Celery worker starts in Docker Compose
- [ ] Celery Beat scheduler runs periodic tasks at correct times
- [ ] `recalculate_score` runs after each activity verification
- [ ] Failed tasks retry 3 times with exponential backoff
- [ ] Task results retrievable by task_id for polling
- [ ] Dead-letter queue for tasks that fail all retries
- [ ] Celery Flower monitoring available at `localhost:5555` in dev
