import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from app.api.v1.endpoints import health as health_endpoint
from app.api.v1.router import api_v1_router
from app.core.config import settings
from app.core.logging import setup_logging
from fastapi import FastAPI, Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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

    @app.exception_handler(RequestValidationError)
    async def invalid_input(request: Request, exc: RequestValidationError):
        if request.url.path != "/api/v1/auth/login":
            return await request_validation_exception_handler(request, exc)
        # Pydantic includes rejected input values, which may contain a password.
        return JSONResponse(status_code=422, content={"detail": "Dados inválidos."})

    @app.middleware("http")
    async def private_responses(request: Request, call_next):
        response = await call_next(request)
        if request.url.path.startswith(("/api/v1/auth/", "/api/v1/teams/")):
            response.headers["Cache-Control"] = "private, no-store"
        return response

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
