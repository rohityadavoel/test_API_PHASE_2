"""
User schemas.
"""
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import Literal

class UserBase(BaseModel):
    """Base fields for User."""
    name: str = Field(..., max_length=120)
    email: EmailStr
    role: Literal["client", "consultant", "admin"]

class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8)

class UserRead(UserBase):
    """Schema for returning user data."""
    id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}

class UserLogin(BaseModel):
    """Schema for logging in a user."""
    email: EmailStr
    password: str
