from datetime import UTC, datetime
from typing import Literal

from app.core.config import settings
from app.db.session import check_db_connection, get_db
from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


class HealthResponse(BaseModel):
    status: Literal["healthy", "degraded"] = Field(
        description="Overall service health status"
    )
    app_name: str = Field(description="Name of the application")
    version: str = Field(description="Application semantic version")
    environment: str = Field(description="Runtime environment")
    timestamp: datetime = Field(description="Current UTC timestamp")
    database: Literal["connected", "disconnected"] = Field(
        description="Database connectivity status"
    )


@router.get(
    "/health",
    response_model=HealthResponse,
    responses={503: {"model": HealthResponse, "description": "Database unavailable"}},
    summary="Health check probe",
    description="Returns service availability, version, and database connectivity.",
)
async def get_health(
    response: Response, session: AsyncSession = Depends(get_db)
) -> HealthResponse:
    db_ok = await check_db_connection(session)
    if not db_ok:
        response.status_code = 503
    return HealthResponse(
        status="healthy" if db_ok else "degraded",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        timestamp=datetime.now(UTC),
        database="connected" if db_ok else "disconnected",
    )
