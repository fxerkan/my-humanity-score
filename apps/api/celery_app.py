"""Celery application factory for MHS background jobs."""

from celery import Celery
from celery.schedules import crontab

from core.config import settings

app = Celery(
    "mhs",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=[
        "tasks.scoring",
        "tasks.verification",
        "tasks.sync",
        "tasks.angel_ai",
    ],
)

app.conf.update(
    # Serialization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    # Timezone
    timezone="UTC",
    enable_utc=True,
    # Results
    result_expires=86400,  # 24 h
    task_track_started=True,
    # Retry / reliability
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,
    # Dead-letter queue: tasks that exhaust all retries go to dead_letter queue
    task_queues={
        "default": {
            "exchange": "default",
            "routing_key": "default",
            "queue_arguments": {
                "x-dead-letter-exchange": "dead_letter",
                "x-dead-letter-routing-key": "dead_letter",
            },
        },
        "dead_letter": {
            "exchange": "dead_letter",
            "routing_key": "dead_letter",
        },
        "scoring": {
            "exchange": "scoring",
            "routing_key": "scoring",
            "queue_arguments": {
                "x-dead-letter-exchange": "dead_letter",
                "x-dead-letter-routing-key": "dead_letter",
            },
        },
    },
    task_default_queue="default",
    task_routes={
        "tasks.scoring.*": {"queue": "scoring"},
        "tasks.verification.*": {"queue": "default"},
        "tasks.sync.*": {"queue": "default"},
        "tasks.angel_ai.*": {"queue": "default"},
    },
    # Beat schedule
    beat_schedule={
        "daily-score-recalculation": {
            "task": "tasks.scoring.recalculate_stale_scores",
            "schedule": crontab(hour=3, minute=0),  # 03:00 UTC daily
        },
        "weekly-carbon-update": {
            "task": "tasks.scoring.update_carbon_scores",
            "schedule": crontab(day_of_week=1, hour=2, minute=0),  # Monday 02:00
        },
        "monthly-mentor-summaries": {
            "task": "tasks.angel_ai.generate_monthly_summaries",
            "schedule": crontab(day_of_month=1, hour=6, minute=0),  # 1st of month
        },
    },
)
