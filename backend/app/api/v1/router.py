from app.api.v1.endpoints import health
from app.modules.auth import router as auth
from app.modules.teams import router as teams
from fastapi import APIRouter

api_v1_router = APIRouter()
api_v1_router.include_router(health.router, tags=["Health"])
api_v1_router.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
api_v1_router.include_router(teams.router, prefix="/teams", tags=["Equipes"])
