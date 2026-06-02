import uuid
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from app.models.consultation import Consultation, StatusEnum
from app.models.user import User, RoleEnum
from app.schemas.consultation import ConsultationCreate, ConsultationUpdate, ConsultationFilter

async def create_consultation(db: AsyncSession, client_id: uuid.UUID, data: ConsultationCreate) -> Consultation:
    # Verify consultant exists and has consultant role
    result = await db.execute(select(User).where(User.id == data.consultant_id))
    consultant = result.scalars().first()
    if not consultant or consultant.role != RoleEnum.consultant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consultant not found")

    new_consultation = Consultation(
        client_id=client_id,
        consultant_id=data.consultant_id,
        scheduled_at=data.scheduled_at,
        duration_minutes=data.duration_minutes,
        notes=data.notes,
        status=StatusEnum.pending
    )
    db.add(new_consultation)
    await db.commit()
    await db.refresh(new_consultation)
    return new_consultation

async def get_consultation(db: AsyncSession, consultation_id: uuid.UUID, current_user: User) -> Consultation:
    result = await db.execute(select(Consultation).where(Consultation.id == consultation_id))
    consultation = result.scalars().first()
    if not consultation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consultation not found")
    
    if current_user.role == RoleEnum.client and consultation.client_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this consultation")
    if current_user.role == RoleEnum.consultant and consultation.consultant_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this consultation")
        
    return consultation

async def list_consultations(db: AsyncSession, current_user: User, filters: ConsultationFilter) -> list[Consultation]:
    query = select(Consultation)
    
    if current_user.role == RoleEnum.client:
        query = query.where(Consultation.client_id == current_user.id)
    else:
        query = query.where(Consultation.consultant_id == current_user.id)
        
    if filters.status:
        query = query.where(Consultation.status == filters.status)
    if filters.consultant_id and current_user.role == RoleEnum.client:
        query = query.where(Consultation.consultant_id == filters.consultant_id)
    if filters.from_date:
        query = query.where(Consultation.scheduled_at >= filters.from_date)
    if filters.to_date:
        query = query.where(Consultation.scheduled_at <= filters.to_date)
        
    result = await db.execute(query)
    return result.scalars().all()

async def update_consultation(db: AsyncSession, consultation_id: uuid.UUID, data: ConsultationUpdate, current_user: User) -> Consultation:
    consultation = await get_consultation(db, consultation_id, current_user)
    
    if data.scheduled_at is not None:
        consultation.scheduled_at = data.scheduled_at
    if data.duration_minutes is not None:
        consultation.duration_minutes = data.duration_minutes
    if data.notes is not None:
        consultation.notes = data.notes
    if data.status is not None:
        consultation.status = data.status
        
    await db.commit()
    await db.refresh(consultation)
    return consultation

async def delete_consultation(db: AsyncSession, consultation_id: uuid.UUID, current_user: User) -> None:
    consultation = await get_consultation(db, consultation_id, current_user)
    
    if consultation.status != StatusEnum.pending:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Can only delete pending consultations")
        
    await db.delete(consultation)
    await db.commit()
