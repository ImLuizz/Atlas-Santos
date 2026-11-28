from app.modules.auth.models import User, UserRole
from app.modules.photos.models import Photo, PhotoStatus
from app.modules.photos.schemas import PhotoResponse
from sqlalchemy import select


def photo_response(photo: Photo) -> PhotoResponse:
    show_location = photo.status == PhotoStatus.APPROVED and photo.location_authorized
    return PhotoResponse(
        id=photo.id,
        owner_id=photo.owner_id,
        team_id=photo.team_id,
        status=photo.status,
        caption=photo.caption,
        reflection=photo.reflection,
        ai_description=photo.ai_description,
        rejection_reason=photo.rejection_reason,
        captured_at=photo.captured_at,
        latitude=photo.latitude if show_location else None,
        longitude=photo.longitude if show_location else None,
        travel_day=photo.travel_day,
        theme_id=photo.theme_id,
    )


def gallery_query(user: User, include_pending: bool):
    query = select(Photo).where(Photo.status != PhotoStatus.REMOVED)
    if not include_pending or user.role == UserRole.PARTICIPANTE:
        query = query.where(Photo.status == PhotoStatus.APPROVED)
    elif user.role == UserRole.CAPITAO:
        query = query.where(
            (Photo.status == PhotoStatus.APPROVED) | (Photo.team_id == user.team_id)
        )
    return query


def can_view_image(user: User, photo: Photo) -> bool:
    allowed = photo.status == PhotoStatus.APPROVED or photo.owner_id == user.id
    if user.role == UserRole.CAPITAO:
        allowed = allowed or user.team_id == photo.team_id
    if user.role == UserRole.ADMINISTRACAO:
        allowed = True
    return allowed
