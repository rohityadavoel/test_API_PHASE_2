"""
Consultation service for booking and status transitions.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.models.consultation import Consultation
from app.schemas.consultation import ConsultationCreate

async def create_consultation(db: AsyncSession, client_id: UUID, consultation_in: ConsultationCreate) -> Consultation:
    """Book a new consultation."""
    db_consultation = Consultation(
        client_id=client_id,
        consultant_id=consultation_in.consultant_id,
        scheduled_at=consultation_in.scheduled_at,
        notes=consultation_in.notes,
        status="pending"
    )
    db.add(db_consultation)
    await db.commit()
    await db.refresh(db_consultation)
    return db_consultation
