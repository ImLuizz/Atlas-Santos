"""Contas, equipes e sessões do Atlas. Preserva a fila existente."""

import sqlalchemy as sa
from alembic import op

revision = "access2a001"
down_revision = "45e99ca9977f"
branch_labels = None
depends_on = None

role = sa.Enum("PARTICIPANTE", "CAPITAO", "ADMINISTRACAO", name="userrole")
kind = sa.Enum("ESTUDANTE", "SERVIDOR", name="participantkind")


def upgrade() -> None:
    op.create_table(
        "teams",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False, unique=True),
        sa.Column("atlas_name", sa.String(120), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("name", sa.String(160), nullable=False),
        sa.Column("role", role, nullable=False),
        sa.Column("participant_kind", kind, nullable=False),
        sa.Column("team_id", sa.String(36), sa.ForeignKey("teams.id")),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("photo_quota", sa.Integer(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "team_id IS NOT NULL OR role = 'ADMINISTRACAO'", name="ck_user_team"
        ),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_team_id", "users", ["team_id"])
    condition = sa.text("role = 'CAPITAO'")
    op.create_index(
        "uq_users_team_captain",
        "users",
        ["team_id"],
        unique=True,
        postgresql_where=condition,
        sqlite_where=condition,
    )
    op.create_table(
        "sessions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("token_hash", sa.String(64), nullable=False, unique=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_sessions_user_id", "sessions", ["user_id"])


def downgrade() -> None:
    op.drop_table("sessions")
    op.drop_table("users")
    op.drop_table("teams")
    kind.drop(op.get_bind(), checkfirst=True)
    role.drop(op.get_bind(), checkfirst=True)
