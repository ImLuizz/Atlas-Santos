from datetime import UTC, datetime

from app.core.config import settings
from app.core.security import hash_token
from app.db.session import get_db
from app.modules.auth.models import Session, User, UserRole
from fastapi import Cookie, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


def active_accounts():
    query = select(User).where(User.active.is_(True))
    if not settings.allows_test_accounts:
        # atlas.test is reserved for the development and staging fixtures.
        query = query.where(User.email.not_ilike("%@atlas.test"))
    return query


async def get_current_user(
    atlas_session: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not atlas_session:
        raise HTTPException(status_code=401, detail="Autenticação necessária.")
    user = await db.scalar(
        active_accounts()
        .join(Session)
        .where(
            Session.token_hash == hash_token(atlas_session),
            Session.revoked_at.is_(None),
            Session.expires_at > datetime.now(UTC),
        )
    )
    if user is None:
        raise HTTPException(status_code=401, detail="Sessão inválida ou expirada.")
    return user


async def require_team_captain(
    team_id: str, user: User = Depends(get_current_user)
) -> User:
    if user.role != UserRole.CAPITAO or user.team_id != team_id:
        raise HTTPException(
            status_code=403, detail="Acesso reservado à capitania da equipe."
        )
    return user
