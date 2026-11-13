import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from app.api.v1.endpoints import health as health_endpoint
from app.api.v1.router import api_v1_router
from app.core.config import settings
from app.core.logging import setup_logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application startup and shutdown events."""
    setup_logging()
    logger.info(
        f"Starting {settings.APP_NAME} v{settings.APP_VERSION} [{settings.ENVIRONMENT}]"
    )
    yield
    logger.info(f"Shutting down {settings.APP_NAME}")


def create_app() -> FastAPI:
    """FastAPI Application factory."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "Atlas Santos Backend API — Monólito Modular para Cartografia Colaborativa "
            "do Estudo do Meio em Santos (05-11/10/2026)."
        ),
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # CORS Middleware
    if settings.CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Root health endpoint (for platforms/load balancers e.g. Railway)
    app.include_router(health_endpoint.router, tags=["Health"])

    # API v1 Router
    app.include_router(api_v1_router, prefix="/api/v1")

    return app


app = create_app()
