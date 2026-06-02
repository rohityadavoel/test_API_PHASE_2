import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from app.models.consultation import StatusEnum

class ConsultationCreate(BaseModel):
    consultant_id: uuid.UUID
    scheduled_at: datetime
    duration_minutes: int
    notes: Optional[str] = None

class ConsultationUpdate(BaseModel):
    scheduled_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    notes: Optional[str] = None
    status: Optional[StatusEnum] = None

class ConsultationResponse(BaseModel):
    id: uuid.UUID
    client_id: uuid.UUID
    consultant_id: uuid.UUID
    scheduled_at: datetime
    duration_minutes: int
    status: StatusEnum
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ConsultationFilter(BaseModel):
    status: Optional[StatusEnum] = None
    consultant_id: Optional[uuid.UUID] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
