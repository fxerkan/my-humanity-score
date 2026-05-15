"""Background tasks for Angel AI (Guardian + Mentor modules)."""

import logging

from celery_app import app

logger = logging.getLogger(__name__)


@app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=300,
    retry_jitter=True,
    soft_time_limit=30,
)
def guardian_analyze(self, content: str, user_id: str) -> dict[str, str]:
    """Async Guardian check — analyse content for toxicity/ethics violations.

    Raw toxicity score is NEVER returned to the client; only a bucket
    ("low" | "medium" | "high") is exposed.

    Args:
        content: Text content submitted by the user (activity description, comment).
        user_id: UUID string of the submitting user.

    Returns:
        Dict with user_id, bucket ("low"|"medium"|"high"), and action taken.
    """
    logger.info("guardian_analyze started for user_id=%s", user_id)
    # Stub: full HuggingFace toxicity model in TASK-012
    bucket = _classify_toxicity_stub(content)
    action = "none" if bucket == "low" else ("flag" if bucket == "medium" else "block")
    result = {"user_id": user_id, "bucket": bucket, "action": action}
    logger.info("guardian_analyze user_id=%s bucket=%s action=%s", user_id, bucket, action)
    return result


def _classify_toxicity_stub(content: str) -> str:
    """Placeholder classifier — always returns 'low'.

    Full ML model integrated in TASK-012.

    Args:
        content: Text to classify.

    Returns:
        Toxicity bucket string.
    """
    _ = content  # unused until TASK-012
    return "low"


@app.task(
    bind=True,
    max_retries=2,
    soft_time_limit=7200,
)
def generate_monthly_summaries(self) -> dict[str, int]:
    """Monthly batch job: generate Angel AI Mentor summaries for all active users.

    Returns:
        Dict with count of summaries generated.
    """
    import asyncio

    from sqlalchemy import select

    from core.database import AsyncSessionLocal
    from models.user import User

    async def _fetch_active_user_ids() -> list[str]:
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(User.id).where(User.is_active.is_(True)))
            return [str(row[0]) for row in result.fetchall()]

    logger.info("generate_monthly_summaries started")
    # Stub: enqueue per-user mentor summaries; full impl in TASK-901
    user_ids = asyncio.run(_fetch_active_user_ids())
    logger.info("generate_monthly_summaries would process %d users", len(user_ids))
    return {"processed": len(user_ids)}
