"""
User ORM model.
"""
import uuid
from datetime import datetime
from sqlalchemy import String, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    """
    User model representing clients, consultants, and admins.
    """
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    role: Mapped[str] = mapped_column(
        Enum("client", "consultant", "admin", name="user_role_enum", create_type=False),
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )

    # Relationships
    client_consultations = relationship(
        "Consultation",
        foreign_keys="Consultation.client_id",
        back_populates="client"
    )
    consultant_consultations = relationship(
        "Consultation",
        foreign_keys="Consultation.consultant_id",
        back_populates="consultant"
    )
    chat_messages = relationship("ChatMessage", back_populates="user")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
