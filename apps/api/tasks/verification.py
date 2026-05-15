"""Background tasks for activity verification pipeline."""

import logging
import uuid

from celery_app import app

logger = logging.getLogger(__name__)

_VERIFICATION_LAYERS = 5


@app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=120,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def verify_activity(self, activity_id: str) -> dict[str, object]:
    """Run the 5-layer verification pipeline for an activity.

    Layers:
        1. URL/domain reputation check
        2. NLP semantic plausibility
        3. Duplicate detection
        4. Organisation email confirmation (async)
        5. Peer review queue placement

    Args:
        activity_id: UUID string of the activity to verify.

    Returns:
        Dict with activity_id, verification_level (0-5), and status.
    """
    import asyncio

    from sqlalchemy import select, update

    from core.database import AsyncSessionLocal
    from models.activity import Activity

    logger.info("verify_activity started for activity_id=%s", activity_id)
    activity_uuid = uuid.UUID(activity_id)

    async def _run_pipeline() -> dict[str, object]:
        async with AsyncSessionLocal() as db:
            activity = await db.scalar(select(Activity).where(Activity.id == activity_uuid))
            if not activity:
                logger.warning("verify_activity: activity %s not found", activity_id)
                return {"activity_id": activity_id, "status": "not_found"}

            # Layer 1-3: auto-verification (stub — full impl in TASK-011)
            verification_level = _auto_verify(activity)

            new_status = "auto_verified" if verification_level >= 3 else "pending"

            await db.execute(
                update(Activity)
                .where(Activity.id == activity_uuid)
                .values(status=new_status, verification_level=verification_level)
            )
            await db.commit()

            if new_status == "auto_verified":
                # Trigger score recalculation
                from tasks.scoring import recalculate_score

                recalculate_score.delay(str(activity.user_id))

            # Layer 4: send org email if evidence_url is present
            if activity.evidence_url and verification_level < 3:
                send_org_email.delay(activity_id)

            return {
                "activity_id": activity_id,
                "verification_level": verification_level,
                "status": new_status,
            }

    try:
        return asyncio.run(_run_pipeline())
    except Exception as exc:
        logger.warning("verify_activity failed activity_id=%s: %s", activity_id, exc)
        raise self.retry(exc=exc)


def _auto_verify(activity: object) -> int:
    """Stub: return a basic verification level based on evidence presence.

    Full NLP/ML pipeline implemented in TASK-011.

    Args:
        activity: Activity ORM instance.

    Returns:
        Verification level integer 0-3.
    """
    level = 0
    if getattr(activity, "evidence_url", None):
        level += 1
    if (
        getattr(activity, "description", None)
        and len(getattr(activity, "description", "") or "") > 50
    ):
        level += 1
    if getattr(activity, "activity_date", None):
        level += 1
    return level


@app.task(
    bind=True,
    max_retries=2,
    default_retry_delay=300,
)
def send_org_email(self, activity_id: str) -> dict[str, str]:
    """Send a verification request email to the organisation listed in evidence_url.

    Args:
        activity_id: UUID string of the activity.

    Returns:
        Dict with activity_id and email status.
    """
    logger.info("send_org_email queued for activity_id=%s", activity_id)
    # Stub: full SMTP implementation in TASK-011
    return {"activity_id": activity_id, "email_status": "queued"}
