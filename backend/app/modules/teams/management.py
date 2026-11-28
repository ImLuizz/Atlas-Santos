from app.core.security import hash_password
from app.db.audit import AuditLog
from app.db.session import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.models import ParticipantKind, User, UserRole
from app.modules.teams.models import Team
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


class TeamCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    atlas_name: str | None = Field(default=None, max_length=120)


class TeamResponse(BaseModel):
    id: str
    name: str
    atlas_name: str | None


class UserCreate(BaseModel):
    email: str = Field(max_length=255)
    name: str = Field(min_length=2, max_length=160)
    role: UserRole
    participant_kind: ParticipantKind
    team_id: str | None = None
    photo_quota: int = Field(default=20, ge=1, le=100)


@router.post("/users", response_model=dict)
async def create_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
    actor: User = Depends(require_roles(UserRole.ADMINISTRACAO)),
):
    existing = (
        await db.execute(
            select(User).where(User.email == payload.email.strip().lower())
        )
    ).scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=409, detail="Já existe uma conta com este e-mail."
        )
    import secrets

    temporary_password = secrets.token_urlsafe(12)
    user = User(
        email=payload.email.strip().lower(),
        name=payload.name,
        role=payload.role,
        participant_kind=payload.participant_kind,
        team_id=payload.team_id,
        photo_quota=payload.photo_quota,
        password_hash=hash_password(temporary_password),
    )
    db.add(user)
    await db.flush()
    db.add(
        AuditLog(
            actor_id=actor.id,
            action="user_created",
            entity_type="user",
            entity_id=user.id,
            details={"role": user.role.value, "team_id": user.team_id},
        )
    )
    await db.commit()
    await db.refresh(user)
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role.value,
        "team_id": user.team_id,
        "temporary_password": temporary_password,
        "delivery": "mock-email-service",
    }


@router.get("", response_model=list[TeamResponse])
async def list_teams(
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(
        require_roles(UserRole.PARTICIPANTE, UserRole.CAPITAO, UserRole.ADMINISTRACAO)
    ),
):
    teams = (await db.execute(select(Team).order_by(Team.name))).scalars().all()
    return [TeamResponse(id=t.id, name=t.name, atlas_name=t.atlas_name) for t in teams]


@router.post("", response_model=TeamResponse)
async def create_team(
    payload: TeamCreate,
    db: AsyncSession = Depends(get_db),
    actor: User = Depends(require_roles(UserRole.ADMINISTRACAO)),
):
    team = Team(
        name=payload.name,
        atlas_name=payload.atlas_name or f"Atlas da equipe {payload.name}",
    )
    db.add(team)
    await db.flush()
    db.add(
        AuditLog(
            actor_id=actor.id,
            action="team_created",
            entity_type="team",
            entity_id=team.id,
            details={"name": team.name},
        )
    )
    await db.commit()
    await db.refresh(team)
    return TeamResponse(
        id=team.id,
        name=team.name,
        atlas_name=team.atlas_name,
    )


@router.post("/{team_id}/captain/{user_id}", response_model=TeamResponse)
async def set_captain(
    team_id: str,
    user_id: str,
    db: AsyncSession = Depends(get_db),
    actor: User = Depends(require_roles(UserRole.ADMINISTRACAO)),
):
    team = await db.get(Team, team_id)
    user = await db.get(User, user_id)
    if team is None or user is None:
        raise HTTPException(status_code=404, detail="Equipe ou usuário não encontrado.")
    if user.team_id != team_id:
        raise HTTPException(status_code=422, detail="O usuário não pertence à equipe.")
    old_role = user.role
    previous = await db.scalar(
        select(User).where(User.team_id == team_id, User.role == UserRole.CAPITAO)
    )
    if previous and previous.id != user.id:
        previous.role = UserRole.PARTICIPANTE
        await db.flush()
    user.role = UserRole.CAPITAO
    db.add(
        AuditLog(
            actor_id=actor.id,
            action="captain_changed",
            entity_type="team",
            entity_id=team.id,
            details={"captain_id": user.id, "previous_role": old_role.value},
        )
    )
    await db.commit()
    await db.refresh(team)
    return TeamResponse(
        id=team.id,
        name=team.name,
        atlas_name=team.atlas_name,
    )
