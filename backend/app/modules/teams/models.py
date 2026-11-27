import uuid
from datetime import UTC, datetime

from app.db.base import Base
from sqlalchemy import (
    DateTime,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    atlas_name: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
