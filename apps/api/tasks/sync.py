"""Background tasks for syncing external platform data."""

import logging

from celery_app import app

logger = logging.getLogger(__name__)


@app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=300,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=1800,
    retry_jitter=True,
)
def sync_github(self, user_id: str) -> dict[str, object]:
    """Import GitHub contributions and open-source activity for a user.

    Fetches: commits, PRs, repo stars, issues closed.
    Creates Activity records for verified open-source contributions.

    Args:
        user_id: UUID string of the user to sync.

    Returns:
        Dict with user_id and count of activities synced.
    """
    logger.info("sync_github started for user_id=%s", user_id)
    # Stub: full GitHub OAuth + API integration in TASK-018
    result = {"user_id": user_id, "synced": 0, "platform": "github"}
    logger.info("sync_github completed user_id=%s synced=%d", user_id, result["synced"])
    return result


@app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=300,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=1800,
    retry_jitter=True,
)
def sync_linkedin(self, user_id: str) -> dict[str, object]:
    """Import LinkedIn volunteer and professional activity for a user.

    Fetches: volunteer roles, certifications, publications.
    Creates Activity records for verified contributions.

    Args:
        user_id: UUID string of the user to sync.

    Returns:
        Dict with user_id and count of activities synced.
    """
    logger.info("sync_linkedin started for user_id=%s", user_id)
    # Stub: full LinkedIn OAuth + API integration in TASK-018
    result = {"user_id": user_id, "synced": 0, "platform": "linkedin"}
    logger.info("sync_linkedin completed user_id=%s synced=%d", user_id, result["synced"])
    return result
