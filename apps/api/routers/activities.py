"""Activity CRUD endpoints."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.deps import get_current_user_id
from models.activity import Activity
from schemas.activity import ActivityCreate, ActivityResponse, ActivityUpdate

router = APIRouter(prefix="/activities", tags=["activities"])


@router.post("/", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
async def create_activity(
    body: ActivityCreate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> Activity:
    activity = Activity(user_id=current_user_id, **body.model_dump())
    db.add(activity)
    await db.commit()
    await db.refresh(activity)
    return activity


@router.get("/", response_model=list[ActivityResponse])
async def list_my_activities(
    limit: int = 20,
    offset: int = 0,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> list[Activity]:
    result = await db.scalars(
        select(Activity)
        .where(Activity.user_id == current_user_id)
        .order_by(desc(Activity.created_at))
        .limit(min(limit, 100))
        .offset(offset)
    )
    return list(result)


@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(
    activity_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> Activity:
    activity = await db.scalar(select(Activity).where(Activity.id == activity_id))
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    if activity.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    return activity


@router.patch("/{activity_id}", response_model=ActivityResponse)
async def update_activity(
    activity_id: uuid.UUID,
    body: ActivityUpdate,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> Activity:
    activity = await db.scalar(select(Activity).where(Activity.id == activity_id))
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    if activity.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    if activity.status != "pending":
        raise HTTPException(status_code=400, detail="Cannot edit a non-pending activity")

    for field, value in body.model_dump(exclude_none=True).items():
        setattr(activity, field, value)
    await db.commit()
    await db.refresh(activity)
    return activity


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity(
    activity_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> None:
    activity = await db.scalar(select(Activity).where(Activity.id == activity_id))
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    if activity.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    await db.delete(activity)
    await db.commit()
