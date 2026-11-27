from app.db.session import get_db
from app.modules.auth.dependencies import active_accounts, require_team_captain
from app.modules.auth.models import ParticipantKind, User, UserRole
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


class MemberResponse(BaseModel):
    id: str
    name: str
    role: UserRole
    participant_kind: ParticipantKind


@router.get("/{team_id}/members", dependencies=[Depends(require_team_captain)])
async def members(
    team_id: str, db: AsyncSession = Depends(get_db)
) -> list[MemberResponse]:
    result = await db.scalars(
        active_accounts().where(User.team_id == team_id).order_by(User.name, User.id)
    )
    return [
        MemberResponse.model_validate(member, from_attributes=True) for member in result
    ]
