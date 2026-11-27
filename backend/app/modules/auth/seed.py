"""Prepare fictitious participants in an explicitly selected non-production database."""

import asyncio
import os

from app.core.config import settings
from app.core.security import hash_password
from app.db.session import async_session_factory
from app.modules.auth.models import ParticipantKind, User, UserRole
from app.modules.teams.models import Team
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

ACCOUNTS = (
    (
        "Centro",
        "ana@atlas.test",
        "Ana Souza",
        ParticipantKind.ESTUDANTE,
        UserRole.PARTICIPANTE,
    ),
    (
        "Centro",
        "marina@atlas.test",
        "Marina Costa",
        ParticipantKind.ESTUDANTE,
        UserRole.CAPITAO,
    ),
    (
        "Orla",
        "caio@atlas.test",
        "Caio Ribeiro",
        ParticipantKind.SERVIDOR,
        UserRole.PARTICIPANTE,
    ),
)


async def seed_accounts(db: AsyncSession) -> None:
    if not settings.allows_test_accounts:
        raise RuntimeError(
            "O cadastro fictício é exclusivo de desenvolvimento e homologação."
        )
    password = os.environ.get("ATLAS_TEST_ACCOUNT_PASSWORD")
    if settings.ENVIRONMENT == "staging" and (not password or len(password) < 12):
        raise RuntimeError(
            "Defina ATLAS_TEST_ACCOUNT_PASSWORD com ao menos 12 caracteres."
        )
    password = password or "Santos2026!"
    if len(password) > 128:
        raise RuntimeError("A senha de teste admite até 128 caracteres.")

    async with db.begin():
        if db.get_bind().dialect.name == "postgresql":
            # Serialize concurrent bootstrap commands on the same database.
            await db.execute(text("SELECT pg_advisory_xact_lock(702026)"))
        for team_name, email, name, kind, role in ACCOUNTS:
            if await db.scalar(select(User.id).where(User.email == email)):
                continue
            team = await db.scalar(select(Team).where(Team.name == team_name))
            if team is None:
                team = Team(name=team_name, atlas_name=f"Atlas da equipe {team_name}")
                db.add(team)
                await db.flush()
            db.add(
                User(
                    email=email,
                    name=name,
                    team_id=team.id,
                    role=role,
                    participant_kind=kind,
                    password_hash=hash_password(password),
                    photo_quota=settings.DEFAULT_PHOTO_QUOTA,
                )
            )
            await db.flush()


async def main() -> None:
    async with async_session_factory() as db:
        await seed_accounts(db)


if __name__ == "__main__":
    asyncio.run(main())
