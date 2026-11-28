import uuid
from datetime import UTC, datetime

from app.db.base import Base
from sqlalchemy import (
    Boolean,
    DateTime,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column


class Theme(Base):
    __tablename__ = "themes"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class TripConclusion(Base):
    __tablename__ = "trip_conclusions"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    draft_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    final_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="draft", nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )
