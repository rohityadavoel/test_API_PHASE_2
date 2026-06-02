import uuid
from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.consultation import ConsultationCreate, ConsultationUpdate, ConsultationResponse, ConsultationFilter
from app.services import consultation_service
from app.services.auth_service import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("", response_model=ConsultationResponse, status_code=status.HTTP_201_CREATED)
async def create_consultation(
    data: ConsultationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await consultation_service.create_consultation(db, current_user.id, data)

@router.get("", response_model=List[ConsultationResponse])
async def list_consultations(
    filters: ConsultationFilter = Depends(),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await consultation_service.list_consultations(db, current_user, filters)

@router.get("/{id}", response_model=ConsultationResponse)
async def get_consultation(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await consultation_service.get_consultation(db, id, current_user)

@router.patch("/{id}", response_model=ConsultationResponse)
async def update_consultation(
    id: uuid.UUID,
    data: ConsultationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await consultation_service.update_consultation(db, id, data, current_user)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_consultation(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await consultation_service.delete_consultation(db, id, current_user)
