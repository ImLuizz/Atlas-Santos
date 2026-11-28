import enum
import uuid
from datetime import UTC, datetime
from typing import Any

from app.db.base import Base
from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column


class PhotoStatus(enum.StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    REMOVED = "removed"


class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    owner_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    team_id: Mapped[str] = mapped_column(
        ForeignKey("teams.id"), nullable=False, index=True
    )
    theme_id: Mapped[str | None] = mapped_column(ForeignKey("themes.id"), nullable=True)
    status: Mapped[PhotoStatus] = mapped_column(
        Enum(PhotoStatus), default=PhotoStatus.PENDING, nullable=False, index=True
    )
    original_key: Mapped[str] = mapped_column(String(255), nullable=False)
    derived_key: Mapped[str] = mapped_column(String(255), nullable=False)
    caption: Mapped[str | None] = mapped_column(Text, nullable=True)
    reflection: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    captured_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    location_authorized: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    travel_day: Mapped[int | None] = mapped_column(Integer, nullable=True)
    exif_present: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    exif_private: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    removed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )
