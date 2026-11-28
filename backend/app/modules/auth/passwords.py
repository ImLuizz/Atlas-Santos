from app.core.security import (
    hash_password,
    verify_password,
)
from app.db.audit import AuditLog
from app.db.session import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import Session, User
from app.modules.auth.router import require_app_request
from app.modules.auth.schemas import (
    PasswordChange,
    PasswordResetRequest,
)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(dependencies=[Depends(require_app_request)])


@router.post("/password/reset/request")
async def password_reset_request(
    payload: PasswordResetRequest, db: AsyncSession = Depends(get_db)
):
    user = (
        await db.execute(select(User).where(User.email == payload.email))
    ).scalar_one_or_none()
    if user:
        db.add(
            AuditLog(
                actor_id=user.id,
                action="password_reset_requested",
                entity_type="user",
                entity_id=user.id,
            )
        )
        await db.commit()
    # The mock email response does not reveal whether an account exists.
    return {
        "ok": True,
        "message": "Se a conta existir, enviaremos instruções por e-mail.",
    }


@router.post("/password/change")
async def change_password(
    payload: PasswordChange,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not verify_password(payload.current_password, user.password_hash):
        raise HTTPException(status_code=401, detail="Senha atual incorreta.")
    user.password_hash = hash_password(payload.new_password)
    db.add(
        AuditLog(
            actor_id=user.id,
            action="password_changed",
            entity_type="user",
            entity_id=user.id,
        )
    )
    await db.execute(delete(Session).where(Session.user_id == user.id))
    await db.commit()
    return {"ok": True, "message": "Senha alterada. Faça login novamente."}
