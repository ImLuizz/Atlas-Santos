from app.api.v1.endpoints import health
from app.core.config import settings
from app.modules.auth import passwords
from app.modules.auth import router as auth
from app.modules.exports import router as exports
from app.modules.photos import router as photos
from app.modules.reflections import ai, themes
from app.modules.routes import router as routes
from app.modules.teams import management
from app.modules.teams import router as teams
from fastapi import APIRouter, Depends, Request

api_v1_router = APIRouter()

# Core system health & probes
api_v1_router.include_router(health.router, tags=["Health"])
api_v1_router.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
api_v1_router.include_router(teams.router, prefix="/teams", tags=["Equipes"])


def protect_write(request: Request) -> None:
    if request.method not in {"GET", "HEAD", "OPTIONS"}:
        auth.require_app_request(request.headers.get("x-atlas-request"))


if settings.ENVIRONMENT in {"development", "test", "staging"}:
    experimental = APIRouter(dependencies=[Depends(protect_write)])
    experimental.include_router(management.router, prefix="/teams", tags=["Equipes"])
    experimental.include_router(passwords.router, prefix="/auth", tags=["Autenticação"])
    experimental.include_router(photos.router, prefix="/photos", tags=["Fotografias"])
    experimental.include_router(
        themes.router, prefix="/themes", tags=["Olhares sobre Santos"]
    )
    experimental.include_router(routes.router, prefix="/routes", tags=["Percursos"])
    experimental.include_router(exports.router, prefix="/exports", tags=["Exportações"])
    experimental.include_router(ai.router, prefix="/ai", tags=["IA e Conclusão"])
    api_v1_router.include_router(experimental)
