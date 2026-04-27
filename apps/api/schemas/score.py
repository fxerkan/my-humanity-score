"""MHS score response schemas."""

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class ScoreResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    total_score: Decimal
    social_impact: Decimal
    environmental: Decimal
    knowledge_innovation: Decimal
    economic_contribution: Decimal
    cultural_artistic: Decimal
    civic_political: Decimal
    score_level: str
    calculated_at: datetime

    model_config = {"from_attributes": True}


class ScoreSummary(BaseModel):
    total_score: Decimal
    score_level: str
    rank: int | None = None
