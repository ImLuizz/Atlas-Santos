import enum
import uuid
from datetime import UTC, datetime

from app.db.base import Base
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column


class UserRole(enum.StrEnum):
    PARTICIPANTE = "participante"
    CAPITAO = "capitao"
    ADMINISTRACAO = "administracao"


class ParticipantKind(enum.StrEnum):
    ESTUDANTE = "estudante"
    SERVIDOR = "servidor"


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(
            "team_id IS NOT NULL OR role = 'ADMINISTRACAO'", name="ck_user_team"
        ),
        Index(
            "uq_users_team_captain",
            "team_id",
            unique=True,
            sqlite_where=text("role = 'CAPITAO'"),
            postgresql_where=text("role = 'CAPITAO'"),
        ),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    participant_kind: Mapped[ParticipantKind] = mapped_column(
        Enum(ParticipantKind), nullable=False
    )
    team_id: Mapped[str | None] = mapped_column(
        ForeignKey("teams.id"), nullable=True, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    photo_quota: Mapped[int] = mapped_column(Integer, default=20, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
