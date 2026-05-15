"""User profile endpoints."""

import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
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


class InspireRequest(BaseModel):
    inspiration_username: str



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


class InspireResponse(BaseModel):
    """Confirmation that an inspiration was recorded."""

    message: str
    follower_id: str
    inspiration_id: str


class RemoveInspireResponse(BaseModel):
    """Confirmation that an inspiration was removed."""

    message: str
    deleted: bool


@router.post("/me/inspire", response_model=InspireResponse, status_code=201)
async def inspire_me(
    body: InspireRequest,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> InspireResponse:
    """Declare that the authenticated user was inspired by another user.

    Creates an ``INSPIRED_BY`` edge in the Neo4j graph from the
    authenticated user to the inspiration target.  Also ensures both
    user nodes exist in the graph.

    Args:
        body: Request containing ``inspiration_username``.
        current_user_id: UUID from the validated JWT.
        db: Async database session.

    Returns:
        InspireResponse with confirmation details.

    Raises:
        HTTPException 404: If the inspiration target user does not exist.
        HTTPException 400: If attempting to self-inspire.
    """
    from services.network_multiplier import add_inspiration

    if body.inspiration_username == "":
        raise HTTPException(status_code=400, detail="inspiration_username is required")

    # Look up the target user in PostgreSQL
    target_user = await db.scalar(
        select(User).where(User.username == body.inspiration_username)
    )
    if not target_user:
        raise HTTPException(status_code=404, detail="Inspiration user not found")

    follower_id = str(current_user_id)
    inspiration_id = str(target_user.id)

    try:
        await add_inspiration(follower_id, inspiration_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return InspireResponse(
        message="Inspiration recorded",
        follower_id=follower_id,
        inspiration_id=inspiration_id,
    )


@router.delete("/me/inspire/{username}", response_model=RemoveInspireResponse)
async def remove_inspire_me(
    username: str,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> RemoveInspireResponse:
    """Remove an inspiration relationship from the authenticated user.

    Args:
        username: The username of the inspiration to remove.
        current_user_id: UUID from the validated JWT.
        db: Async database session.

    Returns:
        RemoveInspireResponse with deletion status.
    """
    from services.network_multiplier import remove_inspiration

    target_user = await db.scalar(select(User).where(User.username == username))
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    deleted = await remove_inspiration(str(current_user_id), str(target_user.id))
    return RemoveInspireResponse(
        message="Inspiration removed" if deleted else "No inspiration found",
        deleted=deleted,
    )


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
