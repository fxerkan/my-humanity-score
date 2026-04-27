"""Activity request/response schemas."""

import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel

VALID_CATEGORIES = {
    "social_impact",
    "environmental",
    "knowledge_innovation",
    "economic_contribution",
    "cultural_artistic",
    "civic_political",
}


class ActivityCreate(BaseModel):
    title: str
    description: str | None = None
    category: str
    subcategory: str | None = None
    evidence_url: str | None = None
    evidence_type: str | None = None
    activity_date: date | None = None

    def model_post_init(self, __context: object) -> None:
        if self.category not in VALID_CATEGORIES:
            raise ValueError(f"category must be one of {VALID_CATEGORIES}")


class ActivityUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    evidence_url: str | None = None
    activity_date: date | None = None


class ActivityResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    description: str | None
    category: str
    subcategory: str | None
    impact_points: Decimal
    status: str
    verification_level: int
    activity_date: date | None
    created_at: datetime

    model_config = {"from_attributes": True}
