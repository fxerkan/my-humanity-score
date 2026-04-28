"""User profile endpoints."""

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.deps import get_current_user_id, get_optional_user_id
from models.activity import Activity
from models.score import MHSScore
from models.user import User
from schemas.activity import ActivityResponse
from schemas.score import ScoreResponse
from schemas.user import UserPublicResponse, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


async def _get_user_or_404(user_id: uuid.UUID, db: AsyncSession) -> User:
    """Fetch a user by primary key or raise 404."""
    user = await db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def _latest_score(user_id: uuid.UUID, db: AsyncSession) -> MHSScore | None:
    """Return the most recent MHSScore for a user, or None."""
    return await db.scalar(
        select(MHSScore)
        .where(MHSScore.user_id == user_id)
        .order_by(desc(MHSScore.calculated_at))
    )


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Return the authenticated user's own profile."""
    return await _get_user_or_404(current_user_id, db)


@router.patch("/me", response_model=UserResponse)
async def update_me(
    body: UserUpdate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Update the authenticated user's profile fields."""
    user = await _get_user_or_404(current_user_id, db)
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user


@router.get("/me/score", response_model=ScoreResponse)
async def get_my_score(
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> MHSScore:
    """Return the authenticated user's latest detailed score breakdown."""
    score = await _latest_score(current_user_id, db)
    if not score:
        raise HTTPException(status_code=404, detail="No score calculated yet")
    return score


@router.get("/me/activities", response_model=list[ActivityResponse])
async def get_my_activities(
    limit: int = 20,
    offset: int = 0,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> list[Activity]:
    """Return the authenticated user's paginated activity history."""
    result = await db.scalars(
        select(Activity)
        .where(Activity.user_id == current_user_id)
        .order_by(desc(Activity.created_at))
        .limit(min(limit, 100))
        .offset(offset)
    )
    return list(result)


@router.get("/{username}", response_model=UserPublicResponse)
async def get_user_by_username(
    username: str,
    _viewer_id: uuid.UUID | None = Depends(get_optional_user_id),
    db: AsyncSession = Depends(get_db),
) -> UserPublicResponse:
    """Return a public user profile including the latest score snapshot."""
    user = await db.scalar(select(User).where(User.username == username))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    score = await _latest_score(user.id, db)

    return UserPublicResponse(
        username=user.username,
        display_name=user.display_name,
        avatar_url=user.avatar_url,
        bio=user.bio,
        country_code=user.country_code,
        created_at=user.created_at,
        score=score,  # type: ignore[arg-type]
    )
