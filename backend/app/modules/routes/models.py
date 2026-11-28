import uuid
from datetime import UTC, datetime
from typing import Any

from app.db.base import Base
from sqlalchemy import (
    JSON,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column


class Route(Base):
    __tablename__ = "routes"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    team_id: Mapped[str] = mapped_column(
        ForeignKey("teams.id"), nullable=False, index=True
    )
    travel_day: Mapped[int] = mapped_column(Integer, nullable=False)
    geometry: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    provider_name: Mapped[str] = mapped_column(String(80), nullable=False)
    estimated_distance_meters: Mapped[float] = mapped_column(
        Float, default=0, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )
