from app.modules.auth.models import ParticipantKind, UserRole
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=128)


class TeamResponse(BaseModel):
    id: str
    name: str
    atlas_name: str


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: UserRole
    participant_kind: ParticipantKind
    team: TeamResponse | None
    photo_quota: int


class PasswordResetRequest(BaseModel):
    email: str = Field(max_length=255)


class PasswordChange(BaseModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)
