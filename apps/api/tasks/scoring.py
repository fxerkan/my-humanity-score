"""Background tasks for MHS score calculation."""

import logging
import uuid
from datetime import UTC, datetime, timedelta

from celery_app import app

logger = logging.getLogger(__name__)

_STALE_THRESHOLD_DAYS = 7


@app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def recalculate_score(self, user_id: str) -> dict[str, object]:
    """Recalculate the MHS score for a single user.

    Args:
        user_id: UUID string of the user whose score should be updated.

    Returns:
        Dict with user_id and new final_score.
    """
    import asyncio

    from services.score_calculator import MHSCalculator

    logger.info("recalculate_score started for user_id=%s", user_id)
    try:
        calculator = MHSCalculator()

        async def _run() -> object:
            return await calculator.calculate(uuid.UUID(user_id))

        result = asyncio.run(_run())
        logger.info(
            "recalculate_score completed user_id=%s score=%.2f",
            user_id,
            result.final_score,
        )
        return {"user_id": user_id, "final_score": result.final_score}
    except Exception as exc:
        logger.warning("recalculate_score failed user_id=%s: %s", user_id, exc)
        raise self.retry(exc=exc)


@app.task(
    bind=True,
    max_retries=1,
    soft_time_limit=3600,
)
def recalculate_stale_scores(self) -> dict[str, int]:
    """Daily batch job: recalculate scores that have not been updated recently.

    Returns:
        Dict with count of enqueued and skipped users.
    """
    import asyncio

    from sqlalchemy import select

    from core.database import AsyncSessionLocal
    from models.score import MHSScore

    cutoff = datetime.now(UTC) - timedelta(days=_STALE_THRESHOLD_DAYS)

    async def _fetch_stale_user_ids() -> list[str]:
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(MHSScore.user_id).where(MHSScore.calculated_at < cutoff)
            )
            return [str(row[0]) for row in result.fetchall()]

    logger.info("recalculate_stale_scores started (cutoff=%s)", cutoff.isoformat())
    stale_ids = asyncio.run(_fetch_stale_user_ids())
    for uid in stale_ids:
        recalculate_score.delay(uid)
    logger.info("recalculate_stale_scores enqueued %d users", len(stale_ids))
    return {"enqueued": len(stale_ids)}


@app.task(
    bind=True,
    max_retries=2,
    soft_time_limit=7200,
)
def update_carbon_scores(self) -> dict[str, int]:
    """Weekly job: refresh carbon footprint data via Climatiq and update scores.

    Returns:
        Dict with updated count.
    """
    import asyncio

    from sqlalchemy import select

    from core.database import AsyncSessionLocal
    from models.user import User

    async def _fetch_all_user_ids() -> list[str]:
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(User.id).where(User.is_active.is_(True)))
            return [str(row[0]) for row in result.fetchall()]

    logger.info("update_carbon_scores started")
    user_ids = asyncio.run(_fetch_all_user_ids())
    # Enqueue individual score recalculations; actual Climatiq call happens in calculator
    for uid in user_ids:
        recalculate_score.delay(uid)
    logger.info("update_carbon_scores enqueued %d users", len(user_ids))
    return {"enqueued": len(user_ids)}
