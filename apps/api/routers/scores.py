"""Score endpoints: public summary, authenticated breakdown, recalculate.

Ethics rules enforced here:
- Raw hidden-factor values (carbon_kg, toxicity_index, penalty amounts,
  multiplier floats) are NEVER included in any response.
- Only client-safe named buckets are returned via HiddenAdjustments.
"""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.deps import get_current_user_id, get_optional_user_id
from models.score import MHSScore
from models.user import User
from schemas.score import (
    BreakdownResponse,
    CategoryDetail,
    HiddenAdjustments,
    LevelInfo,
    RecalculateResponse,
    ScorePublic,
    ScoreResponse,
    _carbon_bucket_from_penalty,
    _consistency_bucket,
    _network_bucket,
    _toxicity_bucket_from_penalty,
    level_info,
)
from services.score_calculator import CATEGORY_WEIGHTS

router = APIRouter(prefix="/scores", tags=["scores"])

# ── Constants ─────────────────────────────────────────────────────────────────

_STUB_GLOBAL_PERCENTILE: float = 50.0  # placeholder until leaderboard statistics land


# ── Helpers ───────────────────────────────────────────────────────────────────


async def _latest_score_for_user(user_id: uuid.UUID, db: AsyncSession) -> MHSScore | None:
    """Return the most recent MHSScore for a user, or None.

    Args:
        user_id: UUID of the user whose score is requested.
        db: Async database session.

    Returns:
        Most recent MHSScore ORM object, or None if no score exists.
    """
    return await db.scalar(
        select(MHSScore).where(MHSScore.user_id == user_id).order_by(desc(MHSScore.calculated_at))
    )


def _build_breakdown(score: MHSScore) -> BreakdownResponse:
    """Convert an MHSScore ORM object to a BreakdownResponse.

    Raw hidden-factor fields (carbon_penalty, toxicity_penalty,
    network_multiplier, consistency_multiplier, geo_equity_multiplier)
    are converted to client-safe buckets and NEVER exposed directly.

    Args:
        score: MHSScore ORM instance.

    Returns:
        BreakdownResponse with category details and hidden-adjustment buckets.
    """
    categories: dict[str, CategoryDetail] = {}
    for cat, weight in CATEGORY_WEIGHTS.items():
        raw_score = float(getattr(score, cat))
        contribution = round(raw_score * weight, 2)
        categories[cat] = CategoryDetail(
            score=raw_score,
            weight=weight,
            contribution=contribution,
        )

    slug = score.score_level
    info = level_info(slug)

    hidden = HiddenAdjustments(
        carbon_bucket=_carbon_bucket_from_penalty(score.carbon_penalty),
        toxicity_bucket=_toxicity_bucket_from_penalty(score.toxicity_penalty),
        network_effect=_network_bucket(score.network_multiplier),
        consistency=_consistency_bucket(score.consistency_multiplier),
        equity_boost=float(score.geo_equity_multiplier) > 1.0,
    )

    return BreakdownResponse(
        final_score=float(score.total_score),
        level=LevelInfo(**info),
        categories=categories,
        hidden_adjustments=hidden,
    )


# ── Endpoints ─────────────────────────────────────────────────────────────────


@router.get("/me/breakdown", response_model=BreakdownResponse)
async def get_my_breakdown(
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> BreakdownResponse:
    """Return the authenticated user's full score breakdown.

    Requires a valid bearer token.  Hidden factor raw values are never
    included — only client-safe bucket labels are returned.

    Args:
        current_user_id: UUID from the validated JWT.
        db: Async database session.

    Returns:
        BreakdownResponse with final_score, level, categories, and
        hidden_adjustments.

    Raises:
        HTTPException 404: If no score has been calculated yet.
    """
    score = await _latest_score_for_user(current_user_id, db)
    if not score:
        raise HTTPException(status_code=404, detail="No score calculated yet")
    return _build_breakdown(score)


@router.post("/me/recalculate", response_model=RecalculateResponse, status_code=202)
async def recalculate_my_score(
    current_user_id: uuid.UUID = Depends(get_current_user_id),
) -> RecalculateResponse:
    """Trigger an async score recalculation for the authenticated user.

    Real Celery wiring is completed in TASK-11.  For now a stub task_id
    is returned so that clients can implement polling without blocking.

    Args:
        current_user_id: UUID from the validated JWT.

    Returns:
        RecalculateResponse with a stub task_id and status ``"queued"``.
    """
    # TASK-11 will replace this stub with a real Celery delay() call.
    stub_task_id = f"stub-{current_user_id}"
    return RecalculateResponse(task_id=stub_task_id, status="queued")


@router.get("/me", response_model=ScoreResponse)
async def get_my_score(
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> MHSScore:
    """Return the authenticated user's latest score (raw ORM view).

    Args:
        current_user_id: UUID from the validated JWT.
        db: Async database session.

    Returns:
        MHSScore ORM object serialised as ScoreResponse.

    Raises:
        HTTPException 404: If no score has been calculated yet.
    """
    score = await _latest_score_for_user(current_user_id, db)
    if not score:
        raise HTTPException(status_code=404, detail="No score calculated yet")
    return score


@router.get("/leaderboard", response_model=list[ScoreResponse])
async def get_leaderboard(
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
) -> list[MHSScore]:
    """Return the top scores on the leaderboard (public endpoint).

    Args:
        limit: Maximum number of results (capped at 100).
        offset: Pagination offset.
        db: Async database session.

    Returns:
        List of MHSScore ORM objects serialised as ScoreResponse.
    """
    result = await db.scalars(
        select(MHSScore).order_by(desc(MHSScore.total_score)).limit(min(limit, 100)).offset(offset)
    )
    return list(result)


@router.get("/{username}", response_model=ScorePublic)
async def get_public_score(
    username: str,
    _viewer_id: uuid.UUID | None = Depends(get_optional_user_id),
    db: AsyncSession = Depends(get_db),
) -> ScorePublic:
    """Return a public score summary for any user — no auth required.

    Args:
        username: The target user's username slug.
        _viewer_id: Optional viewer UUID (unused; injected for future access control).
        db: Async database session.

    Returns:
        ScorePublic with username, final_score, level, global_percentile, and
        calculated_at.

    Raises:
        HTTPException 404: If the user does not exist or has no score yet.
    """
    user = await db.scalar(select(User).where(User.username == username))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    score = await _latest_score_for_user(user.id, db)
    if not score:
        raise HTTPException(status_code=404, detail="No score calculated yet")

    slug = score.score_level
    info = level_info(slug)

    # Global percentile: percentage of users with a lower score than this user.
    # Returns None if there are no scores at all (prevents division by zero).
    total_count: int = await db.scalar(select(func.count()).select_from(MHSScore)) or 0
    lower_count: int = (
        await db.scalar(
            select(func.count())
            .select_from(MHSScore)
            .where(MHSScore.total_score < score.total_score)
        )
        or 0
    )
    global_percentile: float | None = (
        round(lower_count / total_count * 100, 1) if total_count > 0 else None
    )

    return ScorePublic(
        username=user.username,
        final_score=float(score.total_score),
        level=LevelInfo(**info),
        global_percentile=global_percentile,
        calculated_at=score.calculated_at,
    )
