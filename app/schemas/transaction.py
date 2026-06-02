"""
Transaction schemas.
"""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Literal

class TransactionRead(BaseModel):
    """Schema for returning transaction data."""
    id: UUID
    consultation_id: UUID
    amount: float
    currency: str
    status: Literal["pending", "paid", "refunded"]
    paid_at: Optional[datetime]

    model_config = {"from_attributes": True}

class TransactionSummary(BaseModel):
    """Schema for a summary of transactions."""
    total_amount: float
    currency: str
    transaction_count: int
