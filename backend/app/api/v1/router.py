from app.api.v1.endpoints import health
from fastapi import APIRouter

api_v1_router = APIRouter()

# Core system health & probes
api_v1_router.include_router(health.router, tags=["Health"])

# Module routers will be mounted here as domains are implemented
# e.g.:
# api_v1_router.include_router(identity_router, prefix="/auth")
# api_v1_router.include_router(contributions_router, prefix="/contributions")
