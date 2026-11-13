from datetime import UTC, datetime
from typing import Literal

from app.core.config import settings
from app.db.session import check_db_connection
from fastapi import APIRouter
from pydantic import BaseModel, Field

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
    summary="Health check probe",
    description="Returns service availability, version, and database connectivity.",
)
async def get_health() -> HealthResponse:
    db_ok = await check_db_connection()
    return HealthResponse(
        status="healthy" if db_ok else "degraded",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        timestamp=datetime.now(UTC),
        database="connected" if db_ok else "disconnected",
    )
