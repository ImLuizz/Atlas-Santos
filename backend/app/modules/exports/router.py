import json
from io import BytesIO

from app.db.session import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.photos.models import Photo, PhotoStatus
from app.modules.routes.models import Route
from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/geojson")
async def export_geojson(
    team_id: str | None = Query(default=None),
    travel_day: int | None = Query(default=None, ge=1, le=7),
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    photo_query = select(Photo).where(
        Photo.status == PhotoStatus.APPROVED,
        Photo.latitude.is_not(None),
        Photo.longitude.is_not(None),
        Photo.location_authorized.is_(True),
    )
    route_query = select(Route)
    if team_id:
        photo_query = photo_query.where(Photo.team_id == team_id)
        route_query = route_query.where(Route.team_id == team_id)
    if travel_day:
        photo_query = photo_query.where(Photo.travel_day == travel_day)
        route_query = route_query.where(Route.travel_day == travel_day)
    photos = (await db.execute(photo_query)).scalars().all()
    routes = (await db.execute(route_query)).scalars().all()
    features = []
    for photo in photos:
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [photo.longitude, photo.latitude],
                },
                "properties": {
                    "id": photo.id,
                    "team_id": photo.team_id,
                    "travel_day": photo.travel_day,
                    "caption": photo.caption,
                    "authorized": True,
                },
            }
        )
    for route in routes:
        features.append(
            {
                "type": "Feature",
                "geometry": route.geometry,
                "properties": {
                    "id": route.id,
                    "team_id": route.team_id,
                    "travel_day": route.travel_day,
                    "estimated": True,
                    "provider": route.provider_name,
                },
            }
        )
    payload = {
        "type": "FeatureCollection",
        "features": features,
        "attribution": "Atlas Santos",
    }
    return Response(
        content=json.dumps(payload, ensure_ascii=False),
        media_type="application/geo+json",
    )


@router.get("/png")
async def export_png(
    team_id: str | None = Query(default=None),
    travel_day: int | None = Query(default=None, ge=1, le=7),
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    route_query = select(Route)
    photo_query = select(Photo).where(
        Photo.status == PhotoStatus.APPROVED,
        Photo.latitude.is_not(None),
        Photo.longitude.is_not(None),
        Photo.location_authorized.is_(True),
    )
    if team_id:
        route_query = route_query.where(Route.team_id == team_id)
        photo_query = photo_query.where(Photo.team_id == team_id)
    if travel_day:
        route_query = route_query.where(Route.travel_day == travel_day)
        photo_query = photo_query.where(Photo.travel_day == travel_day)
    routes = (await db.execute(route_query)).scalars().all()
    photos = (await db.execute(photo_query)).scalars().all()
    image = Image.new("RGB", (1200, 800), "white")
    draw = ImageDraw.Draw(image)
    all_points = [
        (p.longitude, p.latitude)
        for p in photos
        if p.longitude is not None and p.latitude is not None
    ]
    if all_points:
        min_lon, max_lon = min(p[0] for p in all_points), max(p[0] for p in all_points)
        min_lat, max_lat = min(p[1] for p in all_points), max(p[1] for p in all_points)

        def xy(lon: float, lat: float) -> tuple[int, int]:
            lx = 40 + (lon - min_lon) / max(max_lon - min_lon, 0.000001) * 1120
            ly = 760 - (lat - min_lat) / max(max_lat - min_lat, 0.000001) * 720
            return int(lx), int(ly)

        for route in routes:
            coords = route.geometry.get("coordinates", [])
            if len(coords) >= 2:
                draw.line(
                    [xy(lon, lat) for lon, lat in coords], fill="#2563eb", width=5
                )
        for lon, lat in all_points:
            x, y = xy(lon, lat)
            draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill="#dc2626")
    draw.text((30, 30), "Atlas Santos - recorte autorizado", fill="#111827")
    output = BytesIO()
    image.save(output, format="PNG")
    return Response(content=output.getvalue(), media_type="image/png")


@router.get("/pdf")
async def export_pdf(
    team_id: str | None = Query(default=None),
    travel_day: int | None = Query(default=None, ge=1, le=7),
    _user: User = Depends(get_current_user),
):
    title = f"Atlas Santos | equipe={team_id or 'todas'} | dia={travel_day or 'todos'}"
    output = BytesIO()
    pdf = canvas.Canvas(output, pagesize=A4)
    pdf.setTitle("Atlas Santos")
    pdf.drawString(50, 800, title)
    pdf.drawString(50, 770, "Conteudo aprovado - Atlas Santos")
    pdf.drawString(50, 740, "Creditos cartograficos: Atlas Santos")
    pdf.showPage()
    pdf.save()
    return Response(content=output.getvalue(), media_type="application/pdf")
