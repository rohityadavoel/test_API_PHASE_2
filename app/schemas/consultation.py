"""
Consultation schemas.
"""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Literal

class ConsultationBase(BaseModel):
    """Base fields for Consultation."""
    scheduled_at: datetime
    notes: Optional[str] = None

class ConsultationCreate(ConsultationBase):
    """Schema for creating a consultation."""
    consultant_id: UUID

class ConsultationUpdate(BaseModel):
    """Schema for updating a consultation status."""
    status: Literal["pending", "confirmed", "completed", "cancelled"]
    notes: Optional[str] = None

class ConsultationRead(ConsultationBase):
    """Schema for returning consultation data."""
    id: UUID
    client_id: UUID
    consultant_id: UUID
    status: Literal["pending", "confirmed", "completed", "cancelled"]

    model_config = {"from_attributes": True}
