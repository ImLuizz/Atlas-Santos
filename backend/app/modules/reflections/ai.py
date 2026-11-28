from app.db.audit import AuditLog
from app.db.session import get_db
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.auth.models import User, UserRole
from app.modules.photos.models import Photo, PhotoStatus
from app.modules.reflections.models import TripConclusion
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


class DescriptionProposal(BaseModel):
    text: str
    source: str = "mock-ai"
    confidence: str = "suggestion"


@router.post(
    "/photos/{photo_id}/descriptions", response_model=list[DescriptionProposal]
)
async def suggest_photo_description(
    photo_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    photo = await db.get(Photo, photo_id)
    if photo is None or photo.status == PhotoStatus.REMOVED:
        raise HTTPException(status_code=404, detail="Fotografia não encontrada.")
    if (
        user.role != UserRole.ADMINISTRACAO
        and photo.owner_id != user.id
        and user.team_id != photo.team_id
    ):
        raise HTTPException(status_code=403, detail="Permissão insuficiente.")
    base = "Uma vista registrada durante o estudo do meio."
    if photo.reflection:
        base = "Uma possível leitura da imagem em relação à experiência registrada."
    db.add(
        AuditLog(
            actor_id=user.id,
            action="ai_description_requested",
            entity_type="photo",
            entity_id=photo.id,
        )
    )
    await db.commit()
    return [
        DescriptionProposal(text=base, source="mock-ai"),
        DescriptionProposal(
            text=(
                "Elementos visualmente registrados no local, "
                "sujeitos à confirmação humana."
            ),
            source="mock-ai",
        ),
    ]


class ConclusionReview(BaseModel):
    final_text: str = Field(min_length=20)


@router.post("/conclusion/draft")
async def draft_conclusion(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_roles(UserRole.ADMINISTRACAO)),
):
    reflections = (
        (
            await db.execute(
                select(Photo.reflection).where(
                    Photo.status == PhotoStatus.APPROVED,
                    Photo.reflection.is_not(None),
                    Photo.removed_at.is_(None),
                )
            )
        )
        .scalars()
        .all()
    )
    if len(reflections) < 3:
        return {"status": "insufficient", "draft_text": None}
    conclusion = (
        await db.execute(select(TripConclusion).limit(1))
    ).scalar_one_or_none()
    draft = (
        "Síntese coletiva provisória baseada nas experiências aprovadas. "
        "Relações interpretativas devem ser revistas antes da publicação."
    )
    if conclusion is None:
        conclusion = TripConclusion(draft_text=draft)
        db.add(conclusion)
    else:
        conclusion.draft_text = draft
        conclusion.status = "draft"
    await db.commit()
    await db.refresh(conclusion)
    return {"status": "draft", "id": conclusion.id, "draft_text": conclusion.draft_text}


@router.post("/conclusion/review")
async def review_conclusion(
    payload: ConclusionReview,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_roles(UserRole.ADMINISTRACAO)),
):
    conclusion = (
        await db.execute(select(TripConclusion).limit(1))
    ).scalar_one_or_none()
    if conclusion is None:
        raise HTTPException(status_code=404, detail="Não existe rascunho de conclusão.")
    conclusion.final_text = payload.final_text
    conclusion.status = "approved"
    db.add(
        AuditLog(
            actor_id=admin.id,
            action="conclusion_approved",
            entity_type="trip_conclusion",
            entity_id=conclusion.id,
        )
    )
    await db.commit()
    await db.refresh(conclusion)
    return {
        "status": conclusion.status,
        "id": conclusion.id,
        "final_text": conclusion.final_text,
    }


@router.get("/conclusion")
async def published_conclusion(
    db: AsyncSession = Depends(get_db), _user: User = Depends(get_current_user)
):
    conclusion = (
        await db.execute(
            select(TripConclusion).where(TripConclusion.status == "approved").limit(1)
        )
    ).scalar_one_or_none()
    if conclusion is None:
        return {"status": "unavailable", "final_text": None}
    return {
        "status": "approved",
        "id": conclusion.id,
        "final_text": conclusion.final_text,
    }
