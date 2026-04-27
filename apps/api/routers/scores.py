"""Score endpoints: get current score, leaderboard."""

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.deps import get_current_user_id
from models.score import MHSScore
from schemas.score import ScoreResponse

router = APIRouter(prefix="/scores", tags=["scores"])


@router.get("/me", response_model=ScoreResponse)
async def get_my_score(
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> MHSScore:
    score = await db.scalar(
        select(MHSScore)
        .where(MHSScore.user_id == current_user_id)
        .order_by(desc(MHSScore.calculated_at))
    )
    if not score:
        raise HTTPException(status_code=404, detail="No score calculated yet")
    return score


@router.get("/leaderboard", response_model=list[ScoreResponse])
async def get_leaderboard(
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
) -> list[MHSScore]:
    result = await db.scalars(
        select(MHSScore)
        .order_by(desc(MHSScore.total_score))
        .limit(min(limit, 100))
        .offset(offset)
    )
    return list(result)
