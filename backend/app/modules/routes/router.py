from datetime import UTC, datetime

from app.db.session import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.photos.models import Photo, PhotoStatus
from app.modules.routes.models import Route
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


class RouteResponse(BaseModel):
    team_id: str
    travel_day: int
    geometry: dict
    provider_name: str
    estimated_distance_meters: float


@router.post("/rebuild")
async def rebuild_routes(
    team_id: str | None = Query(default=None),
    travel_day: int | None = Query(default=None, ge=1, le=7),
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    query = select(Photo).where(
        Photo.status == PhotoStatus.APPROVED,
        Photo.latitude.is_not(None),
        Photo.longitude.is_not(None),
        Photo.location_authorized.is_(True),
    )
    if team_id:
        query = query.where(Photo.team_id == team_id)
    if travel_day:
        query = query.where(Photo.travel_day == travel_day)
    photos = (await db.execute(query)).scalars().all()
    grouped: dict[tuple[str, int], list[Photo]] = {}
    for photo in photos:
        if photo.travel_day is not None:
            grouped.setdefault((photo.team_id, photo.travel_day), []).append(photo)
    for (gid, day), items in grouped.items():
        items.sort(key=lambda p: p.captured_at or datetime.now(UTC))
        coordinates = [
            [float(p.longitude), float(p.latitude)] for p in items
        ]  # GeoJSON order
        geometry = {
            "type": "LineString",
            "coordinates": coordinates if len(coordinates) >= 2 else [],
        }
        distance = 0.0
        for first, second in zip(coordinates, coordinates[1:], strict=False):
            distance += (
                ((first[0] - second[0]) * 111_000) ** 2
                + ((first[1] - second[1]) * 111_000) ** 2
            ) ** 0.5
        existing = (
            await db.execute(
                select(Route).where(Route.team_id == gid, Route.travel_day == day)
            )
        ).scalar_one_or_none()
        if existing is None:
            db.add(
                Route(
                    team_id=gid,
                    travel_day=day,
                    geometry=geometry,
                    provider_name="local-fallback",
                    estimated_distance_meters=distance,
                )
            )
        else:
            existing.geometry = geometry
            existing.provider_name = "local-fallback"
            existing.estimated_distance_meters = distance
    await db.commit()
    return {"ok": True, "rebuilt": len(grouped)}


@router.get("", response_model=list[RouteResponse])
async def list_routes(
    team_id: str | None = Query(default=None),
    travel_day: int | None = Query(default=None, ge=1, le=7),
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    query = select(Route)
    if team_id:
        query = query.where(Route.team_id == team_id)
    if travel_day:
        query = query.where(Route.travel_day == travel_day)
    routes = (
        (await db.execute(query.order_by(Route.team_id, Route.travel_day)))
        .scalars()
        .all()
    )
    return [
        RouteResponse(
            team_id=r.team_id,
            travel_day=r.travel_day,
            geometry=r.geometry,
            provider_name=r.provider_name,
            estimated_distance_meters=r.estimated_distance_meters,
        )
        for r in routes
    ]
