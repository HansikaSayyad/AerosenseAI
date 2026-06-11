# backend/schemas/recommendation.py

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# ─────────────────────────────────────────
# RECOMMENDATION RESPONSE
# ─────────────────────────────────────────
class RecommendationResponse(BaseModel):
    id: UUID
    aqi_category: str
    general_advice: Optional[str] = None
    outdoor_activity: Optional[str] = None
    mask_required: Optional[str] = None
    window_advice: Optional[str] = None
    sensitive_groups: Optional[List[str]] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# GENERAL API RESPONSE WRAPPERS
# Standardized responses across all endpoints
# ─────────────────────────────────────────
class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    detail: Optional[str] = None