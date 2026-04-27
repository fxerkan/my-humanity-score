---
id: TASK-20
title: Celery + Redis Background Jobs
status: Done
assignee:
  - '@developer'
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 17:18'
labels:
  - epic001-foundation-&-infrastructure
  - sonnet
  - developer
dependencies:
  - task-3
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
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
<!-- SECTION:DESCRIPTION:END -->

# TASK-020 — Celery + Redis Background Jobs

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Celery worker starts in Docker Compose
- [x] #2 Celery Beat scheduler runs periodic tasks at correct times
- [x] #3 `recalculate_score` runs after each activity verification
- [x] #4 Failed tasks retry 3 times with exponential backoff
- [x] #5 Task results retrievable by task_id for polling
- [x] #6 Dead-letter queue for tasks that fail all retries
- [x] #7 Celery Flower monitoring available at `localhost:5555` in dev
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Rewrite celery_app.py — full config: beat schedule, task routing, dead-letter queue, retry policy
2. Create tasks/ package with scoring.py, verification.py, sync.py, angel_ai.py
3. Add Flower to docker-compose.yml under full profile (port 5555)
4. Add flower to requirements.txt
5. Verify Celery worker command in docker-compose already uses celery_app
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
✅ **QA PASSED**
Celery worker, beat, and flower successfully start in Docker Compose. Code inspection confirms task definitions, routing, and dead-letter queues meet specifications.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Celery + Redis background job infrastructure fully configured.

Changes:
- celery_app.py: rewrote with beat_schedule, task_routes, dead-letter queue config (x-dead-letter-exchange), task_acks_late=True, worker_prefetch_multiplier=1
- tasks/scoring.py: recalculate_score (per-user, 3 retries, exponential backoff), recalculate_stale_scores (daily batch), update_carbon_scores (weekly)
- tasks/verification.py: verify_activity (5-layer pipeline stub, triggers score recalc on success), send_org_email (layer-4 email stub)
- tasks/sync.py: sync_github, sync_linkedin (stubs — full OAuth in TASK-018)
- tasks/angel_ai.py: guardian_analyze (toxicity bucket only, never raw score), generate_monthly_summaries (monthly batch)
- docker-compose.yml: added beat (Celery Beat scheduler) and flower (Flower UI at port 5555) services under --profile full
- requirements.txt: added flower==2.0.1, pytest-cov==6.0.0

All tasks use bind=True with max_retries=3 and exponential backoff. Dead-letter queue configured for exhausted retries.
<!-- SECTION:FINAL_SUMMARY:END -->
