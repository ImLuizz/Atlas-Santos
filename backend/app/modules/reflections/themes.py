from app.db.audit import AuditLog
from app.db.session import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.models import User, UserRole
from app.modules.reflections.models import Theme
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


class ThemeCreate(BaseModel):
    title: str = Field(min_length=2, max_length=160)
    question: str = Field(min_length=3)
    active: bool = True


class ThemeResponse(BaseModel):
    id: str
    title: str
    question: str
    active: bool


@router.get("", response_model=list[ThemeResponse])
async def list_themes(
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(
        require_roles(UserRole.PARTICIPANTE, UserRole.CAPITAO, UserRole.ADMINISTRACAO)
    ),
):
    themes = (
        (await db.execute(select(Theme).where(Theme.active).order_by(Theme.title)))
        .scalars()
        .all()
    )
    return [
        ThemeResponse(id=t.id, title=t.title, question=t.question, active=t.active)
        for t in themes
    ]


@router.post("", response_model=ThemeResponse)
async def create_theme(
    payload: ThemeCreate,
    db: AsyncSession = Depends(get_db),
    actor: User = Depends(require_roles(UserRole.ADMINISTRACAO)),
):
    theme = Theme(title=payload.title, question=payload.question, active=payload.active)
    db.add(theme)
    db.add(
        AuditLog(
            actor_id=actor.id,
            action="theme_created",
            entity_type="theme",
            entity_id=theme.id,
        )
    )
    await db.commit()
    await db.refresh(theme)
    return ThemeResponse(
        id=theme.id, title=theme.title, question=theme.question, active=theme.active
    )
