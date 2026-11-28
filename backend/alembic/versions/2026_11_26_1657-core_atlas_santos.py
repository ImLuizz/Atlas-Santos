"""Add core Atlas Santos domain tables.

Revision ID: coreatlas001
Revises: access2a001
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "coreatlas001"
down_revision: str | None = "access2a001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "themes",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("title", sa.String(160), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
    )
    op.create_table(
        "photos",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("owner_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("team_id", sa.String(36), sa.ForeignKey("teams.id"), nullable=False),
        sa.Column("theme_id", sa.String(36), sa.ForeignKey("themes.id")),
        sa.Column(
            "status",
            sa.Enum("PENDING", "APPROVED", "REJECTED", "REMOVED", name="photostatus"),
            nullable=False,
        ),
        sa.Column("original_key", sa.String(255), nullable=False),
        sa.Column("derived_key", sa.String(255), nullable=False),
        sa.Column("caption", sa.Text()),
        sa.Column("reflection", sa.Text()),
        sa.Column("ai_description", sa.Text()),
        sa.Column("rejection_reason", sa.Text()),
        sa.Column("captured_at", sa.DateTime(timezone=True)),
        sa.Column("latitude", sa.Float()),
        sa.Column("longitude", sa.Float()),
        sa.Column("location_authorized", sa.Boolean(), nullable=False),
        sa.Column("travel_day", sa.Integer()),
        sa.Column("exif_present", sa.Boolean(), nullable=False),
        sa.Column("exif_private", sa.JSON()),
        sa.Column("removed_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_photos_owner_id", "photos", ["owner_id"])
    op.create_index("ix_photos_team_id", "photos", ["team_id"])
    op.create_index("ix_photos_status", "photos", ["status"])
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("actor_id", sa.String(36), sa.ForeignKey("users.id")),
        sa.Column("action", sa.String(80), nullable=False),
        sa.Column("entity_type", sa.String(80), nullable=False),
        sa.Column("entity_id", sa.String(36), nullable=False),
        sa.Column("details", sa.JSON()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "routes",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("team_id", sa.String(36), sa.ForeignKey("teams.id"), nullable=False),
        sa.Column("travel_day", sa.Integer(), nullable=False),
        sa.Column("geometry", sa.JSON(), nullable=False),
        sa.Column("provider_name", sa.String(80), nullable=False),
        sa.Column("estimated_distance_meters", sa.Float(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_routes_team_id", "routes", ["team_id"])
    op.create_table(
        "trip_conclusions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("draft_text", sa.Text()),
        sa.Column("final_text", sa.Text()),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("trip_conclusions")
    op.drop_index("ix_routes_team_id", "routes")
    op.drop_table("routes")
    op.drop_table("audit_logs")
    op.drop_index("ix_photos_status", "photos")
    op.drop_index("ix_photos_team_id", "photos")
    op.drop_index("ix_photos_owner_id", "photos")
    op.drop_table("photos")
    op.drop_table("themes")
    sa.Enum(name="photostatus").drop(op.get_bind(), checkfirst=True)
