"""
Consultation ORM model.
"""
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Consultation(Base):
    """
    Consultation model for 1:1 sessions.
    """
    __tablename__ = "consultations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        index=True,
        nullable=False
    )
    consultant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        index=True,
        nullable=False
    )
    scheduled_at: Mapped[datetime] = mapped_column(index=True, nullable=False)
    status: Mapped[str] = mapped_column(
        Enum("pending", "confirmed", "completed", "cancelled", name="consultation_status_enum", create_type=False),
        nullable=False,
        default="pending"
    )
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    client = relationship("User", foreign_keys=[client_id], back_populates="client_consultations")
    consultant = relationship("User", foreign_keys=[consultant_id], back_populates="consultant_consultations")
    transaction = relationship("Transaction", back_populates="consultation", uselist=False)
    review = relationship("Review", back_populates="consultation", uselist=False)

    def __repr__(self) -> str:
        return f"<Consultation(id={self.id}, status={self.status})>"
