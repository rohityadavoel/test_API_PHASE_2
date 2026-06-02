"""
Review schemas.
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class ReviewBase(BaseModel):
    """Base fields for Review."""
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    """Schema for creating a review."""
    consultation_id: UUID

class ReviewRead(ReviewBase):
    """Schema for returning review data."""
    id: UUID
    consultation_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}
