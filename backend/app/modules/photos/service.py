from datetime import UTC, datetime
from io import BytesIO

from app.core.config import settings
from app.db.audit import AuditLog
from app.integrations.storage.local import local_storage
from app.modules.auth.models import User, UserRole
from app.modules.photos.exif import exif_gps
from app.modules.photos.models import Photo, PhotoStatus
from app.modules.photos.schemas import PhotoEdit
from app.modules.photos.visibility import photo_response
from fastapi import HTTPException, UploadFile
from PIL import Image, ImageOps
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

MAX_IMAGE_SIZE = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}


async def upload_photo(
    *,
    file: UploadFile,
    caption: str | None,
    reflection: str | None,
    theme_id: str | None,
    travel_day: int | None,
    latitude: float | None,
    longitude: float | None,
    captured_at: str | None,
    db: AsyncSession,
    user: User,
):
    if not user.team_id:
        raise HTTPException(status_code=422, detail="Usuário sem equipe vinculada.")
    count = (
        await db.execute(
            select(func.count(Photo.id)).where(
                Photo.owner_id == user.id, Photo.status != PhotoStatus.REMOVED
            )
        )
    ).scalar_one()
    if count >= user.photo_quota:
        raise HTTPException(status_code=409, detail="Cota de fotografias atingida.")
    content = await file.read(MAX_IMAGE_SIZE + 1)
    if len(content) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=413, detail="Arquivo excede o limite permitido."
        )
    if not content:
        raise HTTPException(status_code=422, detail="Arquivo vazio.")
    try:
        source = Image.open(BytesIO(content))
        source.verify()
        source = Image.open(BytesIO(content))
        image_format = source.format
        if image_format not in ALLOWED_FORMATS:
            raise HTTPException(
                status_code=415, detail="Formato de imagem não permitido."
            )
        exif = source.getexif()
        exif_present = bool(exif)
        exif_private = (
            {"camera": exif.get(272), "software": exif.get(305)}
            if exif_present
            else None
        )
        gps_lat, gps_lon = exif_gps(exif)
        captured: datetime | None = None
        for tag in (36867, 36868, 306):
            raw = exif.get(tag)
            if isinstance(raw, str):
                try:
                    captured = datetime.strptime(raw, "%Y:%m:%d %H:%M:%S").replace(
                        tzinfo=UTC
                    )
                    break
                except ValueError:
                    pass
        if captured_at:
            try:
                captured = (
                    datetime.fromisoformat(captured_at).replace(tzinfo=UTC)
                    if captured_at.endswith("Z")
                    else datetime.fromisoformat(captured_at)
                )
            except ValueError:
                raise HTTPException(
                    status_code=422,
                    detail="Data de captura inválida.",
                ) from None
        sanitized = ImageOps.exif_transpose(source).convert("RGB")
        output = BytesIO()
        sanitized.save(output, format="JPEG", quality=88, exif=b"")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=415,
            detail="Arquivo de imagem inválido.",
        ) from None

    photo_id = __import__("uuid").uuid4().hex
    original_key = f"originals/{user.id}/{photo_id}.bin"
    derived_key = f"derived/{user.id}/{photo_id}.jpg"
    await local_storage.put(original_key, content)
    await local_storage.put(derived_key, output.getvalue())
    photo = Photo(
        id=photo_id,
        owner_id=user.id,
        team_id=user.team_id,
        theme_id=theme_id,
        status=PhotoStatus.APPROVED
        if user.role == UserRole.CAPITAO
        else PhotoStatus.PENDING,
        original_key=original_key,
        derived_key=derived_key,
        caption=caption,
        reflection=reflection,
        captured_at=captured,
        latitude=gps_lat if latitude is None else latitude,
        longitude=gps_lon if longitude is None else longitude,
        travel_day=travel_day,
        exif_present=exif_present,
        exif_private=exif_private,
    )
    db.add(photo)
    db.add(
        AuditLog(
            actor_id=user.id,
            action="photo_uploaded",
            entity_type="photo",
            entity_id=photo.id,
            details={"status": photo.status.value},
        )
    )
    await db.commit()
    await db.refresh(photo)
    return photo_response(photo)


async def edit_photo(photo_id: str, payload: PhotoEdit, db: AsyncSession, user: User):
    photo = await db.get(Photo, photo_id)
    if photo is None or photo.status == PhotoStatus.REMOVED:
        raise HTTPException(status_code=404, detail="Fotografia não encontrada.")
    if photo.owner_id != user.id:
        raise HTTPException(
            status_code=403, detail="Você só pode editar seus próprios registros."
        )
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(photo, field, value)
    photo.status = (
        PhotoStatus.APPROVED if user.role == UserRole.CAPITAO else PhotoStatus.PENDING
    )
    photo.rejection_reason = None
    db.add(
        AuditLog(
            actor_id=user.id,
            action="photo_edited",
            entity_type="photo",
            entity_id=photo.id,
        )
    )
    await db.commit()
    await db.refresh(photo)
    return photo_response(photo)


async def delete_photo(photo_id: str, db: AsyncSession, user: User):
    photo = await db.get(Photo, photo_id)
    if photo is None or photo.status == PhotoStatus.REMOVED:
        raise HTTPException(status_code=404, detail="Fotografia não encontrada.")
    if user.role == UserRole.ADMINISTRACAO:
        pass
    elif photo.owner_id == user.id:
        pass
    else:
        raise HTTPException(status_code=403, detail="Permissão insuficiente.")
    photo.status = PhotoStatus.REMOVED
    photo.removed_at = datetime.now(UTC)
    db.add(
        AuditLog(
            actor_id=user.id,
            action="photo_removed",
            entity_type="photo",
            entity_id=photo.id,
        )
    )
    await db.commit()
    await local_storage.delete_object(photo.derived_key)
    await local_storage.delete_object(photo.original_key)
    return {"ok": True}
