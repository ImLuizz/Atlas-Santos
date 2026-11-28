from datetime import datetime

from app.modules.photos.models import PhotoStatus
from pydantic import BaseModel, Field


class PhotoResponse(BaseModel):
    id: str
    owner_id: str
    team_id: str
    status: PhotoStatus
    caption: str | None
    reflection: str | None
    ai_description: str | None
    rejection_reason: str | None
    captured_at: datetime | None
    latitude: float | None
    longitude: float | None
    travel_day: int | None
    theme_id: str | None


class PhotoEdit(BaseModel):
    caption: str | None = Field(default=None, max_length=500)
    reflection: str | None = Field(default=None, max_length=5000)
    theme_id: str | None = None
    travel_day: int | None = Field(default=None, ge=1, le=7)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    captured_at: datetime | None = None
    ai_description: str | None = Field(default=None, max_length=2000)


class CurationDecision(BaseModel):
    reason: str | None = Field(default=None, max_length=2000)
