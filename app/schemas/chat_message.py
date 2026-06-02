"""
Chat Message schemas.
"""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Literal

class ChatMessageBase(BaseModel):
    """Base fields for Chat Message."""
    content: str

class ChatMessageCreate(ChatMessageBase):
    """Schema for creating a chat message."""
    pass

class ChatMessageRead(ChatMessageBase):
    """Schema for returning chat message data."""
    id: UUID
    user_id: UUID
    role: Literal["user", "assistant"]
    intent: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
