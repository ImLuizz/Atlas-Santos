from datetime import UTC, datetime

from app.core.config import settings
from app.core.security import (
    generate_secure_token,
    hash_password,
    hash_token,
    session_expiry,
    verify_password,
)
from app.db.session import get_db
from app.modules.auth.dependencies import active_accounts, get_current_user
from app.modules.auth.models import Session, User
from app.modules.auth.schemas import LoginRequest, TeamResponse, UserResponse
from app.modules.teams.models import Team
from fastapi import APIRouter, Cookie, Depends, Header, HTTPException, Response
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool

router = APIRouter()
DUMMY_HASH = hash_password(generate_secure_token())


def require_app_request(x_atlas_request: str | None = Header(default=None)) -> None:
    # Cross-origin browser scripts need a successful CORS preflight for this header.
    if x_atlas_request != "1":
        raise HTTPException(status_code=403, detail="Origem da solicitação inválida.")


async def account_response(user: User, db: AsyncSession) -> UserResponse:
    team = await db.get(Team, user.team_id) if user.team_id else None
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        role=user.role,
        participant_kind=user.participant_kind,
        team=TeamResponse.model_validate(team, from_attributes=True) if team else None,
        photo_quota=user.photo_quota,
    )


@router.post("/login", dependencies=[Depends(require_app_request)])
async def login(
    payload: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
    atlas_session: str | None = Cookie(default=None),
) -> UserResponse:
    email = payload.email.strip().lower()
    user = await db.scalar(active_accounts().where(User.email == email))
    valid = await run_in_threadpool(
        verify_password, payload.password, user.password_hash if user else DUMMY_HASH
    )
    if not valid or user is None:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")
    if atlas_session:
        await revoke_session(atlas_session, db)
    token = generate_secure_token()
    minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    db.add(
        Session(
            user_id=user.id,
            token_hash=hash_token(token),
            expires_at=session_expiry(minutes),
        )
    )
    account = await account_response(user, db)
    await db.commit()
    response.set_cookie(
        "atlas_session",
        token,
        path="/api/v1",
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=minutes * 60,
    )
    return account


async def revoke_session(token: str, db: AsyncSession) -> None:
    await db.execute(
        update(Session)
        .where(Session.token_hash == hash_token(token), Session.revoked_at.is_(None))
        .values(revoked_at=datetime.now(UTC))
    )


@router.post("/logout", dependencies=[Depends(require_app_request)])
async def logout(
    response: Response,
    atlas_session: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
) -> dict[str, bool]:
    if atlas_session:
        await revoke_session(atlas_session, db)
        await db.commit()
    response.delete_cookie(
        "atlas_session",
        path="/api/v1",
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
    )
    return {"ok": True}


@router.get("/me")
async def me(
    user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
) -> UserResponse:
    return await account_response(user, db)
