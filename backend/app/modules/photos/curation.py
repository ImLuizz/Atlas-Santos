from app.db.audit import AuditLog
from app.db.session import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.models import User, UserRole
from app.modules.photos.models import Photo, PhotoStatus
from app.modules.photos.schemas import CurationDecision, PhotoResponse
from app.modules.photos.visibility import photo_response
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/curation/queue", response_model=list[PhotoResponse])
async def curation_queue(
    db: AsyncSession = Depends(get_db),
    captain: User = Depends(require_roles(UserRole.CAPITAO)),
):
    if not captain.team_id:
        raise HTTPException(status_code=422, detail="Capitão sem equipe vinculada.")
    photos = (
        (
            await db.execute(
                select(Photo)
                .where(
                    Photo.team_id == captain.team_id,
                    Photo.status == PhotoStatus.PENDING,
                )
                .order_by(Photo.created_at)
            )
        )
        .scalars()
        .all()
    )
    return [photo_response(p) for p in photos]


@router.post("/{photo_id}/approve", response_model=PhotoResponse)
async def approve_photo(
    photo_id: str,
    db: AsyncSession = Depends(get_db),
    captain: User = Depends(require_roles(UserRole.CAPITAO)),
):
    photo = await db.get(Photo, photo_id)
    if photo is None or photo.status == PhotoStatus.REMOVED:
        raise HTTPException(status_code=404, detail="Fotografia não encontrada.")
    if photo.team_id != captain.team_id:
        raise HTTPException(
            status_code=403, detail="Fotografia pertence a outra equipe."
        )
    photo.status = PhotoStatus.APPROVED
    photo.rejection_reason = None
    db.add(
        AuditLog(
            actor_id=captain.id,
            action="photo_approved",
            entity_type="photo",
            entity_id=photo.id,
        )
    )
    await db.commit()
    await db.refresh(photo)
    return photo_response(photo)


@router.post("/{photo_id}/reject", response_model=PhotoResponse)
async def reject_photo(
    photo_id: str,
    payload: CurationDecision,
    db: AsyncSession = Depends(get_db),
    captain: User = Depends(require_roles(UserRole.CAPITAO)),
):
    if payload.reason is None or not payload.reason.strip():
        raise HTTPException(status_code=422, detail="Justificativa obrigatória.")
    photo = await db.get(Photo, photo_id)
    if photo is None or photo.status == PhotoStatus.REMOVED:
        raise HTTPException(status_code=404, detail="Fotografia não encontrada.")
    if photo.team_id != captain.team_id:
        raise HTTPException(
            status_code=403, detail="Fotografia pertence a outra equipe."
        )
    photo.status = PhotoStatus.REJECTED
    photo.rejection_reason = payload.reason.strip()
    db.add(
        AuditLog(
            actor_id=captain.id,
            action="photo_rejected",
            entity_type="photo",
            entity_id=photo.id,
            details={"reason": photo.rejection_reason},
        )
    )
    await db.commit()
    await db.refresh(photo)
    return photo_response(photo)
