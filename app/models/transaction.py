"""
Transaction ORM model.
"""
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Numeric, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Transaction(Base):
    """
    Transaction model for tracking payments of consultations.
    """
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    consultation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("consultations.id", ondelete="RESTRICT"),
        nullable=False
    )
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    status: Mapped[str] = mapped_column(
        Enum("pending", "paid", "refunded", name="transaction_status_enum", create_type=False),
        nullable=False,
        default="pending"
    )
    paid_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    # Relationships
    consultation = relationship("Consultation", back_populates="transaction")

    def __repr__(self) -> str:
        return f"<Transaction(id={self.id}, amount={self.amount}, status={self.status})>"
