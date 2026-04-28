"""MHS score response schemas."""

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ScoreResponse(BaseModel):
    """Public score response — field names follow the AC contract.

    ORM columns (total_score, score_level) are mapped via validation_alias
    so the API surface uses the spec names (final_score, level) while the
    DB schema stays unchanged.
    """

    id: uuid.UUID
    user_id: uuid.UUID
    final_score: Decimal = Field(validation_alias="total_score")
    social_impact: Decimal
    environmental: Decimal
    knowledge_innovation: Decimal
    economic_contribution: Decimal
    cultural_artistic: Decimal
    civic_political: Decimal
    level: str = Field(validation_alias="score_level")
    calculated_at: datetime

    model_config = {"from_attributes": True, "populate_by_name": True}


class ScoreSummary(BaseModel):
    final_score: Decimal = Field(validation_alias="total_score")
    level: str = Field(validation_alias="score_level")
    rank: int | None = None

    model_config = {"from_attributes": True, "populate_by_name": True}
