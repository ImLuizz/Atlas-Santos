import logging
from collections.abc import AsyncGenerator

from app.core.config import settings
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

logger = logging.getLogger(__name__)

# Normalize sqlite URL for async if needed in tests
database_url = settings.DATABASE_URL
if database_url.startswith("sqlite://") and not database_url.startswith(
    "sqlite+aiosqlite://"
):
    database_url = database_url.replace("sqlite://", "sqlite+aiosqlite://", 1)

# Configure engine kwargs based on dialect
engine_kwargs = {"echo": settings.DATABASE_ECHO}
if not database_url.startswith("sqlite"):
    engine_kwargs.update(
        {
            "pool_size": settings.DATABASE_POOL_SIZE,
            "max_overflow": settings.DATABASE_MAX_OVERFLOW,
            "pool_pre_ping": True,
        }
    )

engine = create_async_engine(database_url, **engine_kwargs)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an active database session."""
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def check_db_connection() -> bool:
    """Verifies that the database is reachable and accepting queries."""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as exc:
        logger.warning(f"Database health check failed: {exc}")
        return False
