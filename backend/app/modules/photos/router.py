from typing import Annotated

from app.db.session import get_db
from app.integrations.storage.local import local_storage
from app.modules.auth.dependencies import get_current_user, require_roles
from app.modules.auth.models import User, UserRole
from app.modules.photos import curation, service
from app.modules.photos.models import Photo, PhotoStatus
from app.modules.photos.schemas import PhotoEdit, PhotoResponse
from app.modules.photos.visibility import can_view_image, gallery_query, photo_response
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("", response_model=list[PhotoResponse])
async def gallery(
    team_id: str | None = Query(default=None),
    travel_day: int | None = Query(default=None, ge=1, le=7),
    include_pending: bool = Query(default=False),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    query = gallery_query(user, include_pending)
    if team_id:
        query = query.where(Photo.team_id == team_id)
    if travel_day:
        query = query.where(Photo.travel_day == travel_day)
    query = query.order_by(
        Photo.captured_at.desc().nullslast(), Photo.created_at.desc()
    )
    photos = (await db.execute(query)).scalars().all()
    return [photo_response(p) for p in photos]


@router.post("", response_model=PhotoResponse)
async def upload_photo(
    file: Annotated[UploadFile, File(...)],
    caption: Annotated[str | None, Form(max_length=500)] = None,
    reflection: Annotated[str | None, Form(max_length=5000)] = None,
    theme_id: Annotated[str | None, Form()] = None,
    travel_day: Annotated[int | None, Form(ge=1, le=7)] = None,
    latitude: Annotated[float | None, Form()] = None,
    longitude: Annotated[float | None, Form()] = None,
    captured_at: Annotated[str | None, Form()] = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles(UserRole.PARTICIPANTE, UserRole.CAPITAO)),
):
    return await service.upload_photo(
        file=file,
        caption=caption,
        reflection=reflection,
        theme_id=theme_id,
        travel_day=travel_day,
        latitude=latitude,
        longitude=longitude,
        captured_at=captured_at,
        db=db,
        user=user,
    )


@router.patch("/{photo_id}", response_model=PhotoResponse)
async def edit_photo(
    photo_id: str,
    payload: PhotoEdit,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await service.edit_photo(
        photo_id=photo_id, payload=payload, db=db, user=user
    )


@router.delete("/{photo_id}")
async def delete_photo(
    photo_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await service.delete_photo(photo_id=photo_id, db=db, user=user)


@router.get("/{photo_id}/image")
async def photo_image(
    photo_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    photo = await db.get(Photo, photo_id)
    if photo is None or photo.status == PhotoStatus.REMOVED:
        raise HTTPException(status_code=404, detail="Fotografia não encontrada.")
    if not can_view_image(user, photo):
        raise HTTPException(
            status_code=403, detail="Fotografia não autorizada para exibição."
        )
    content = await local_storage.get(photo.derived_key)
    if content is None:
        raise HTTPException(status_code=404, detail="Arquivo derivado não disponível.")
    return Response(
        content=content,
        media_type="image/jpeg",
        headers={"Cache-Control": "private, max-age=300"},
    )


router.include_router(curation.router)
