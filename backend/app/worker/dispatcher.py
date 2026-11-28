import asyncio
import logging
from collections.abc import Callable, Coroutine
from datetime import UTC, datetime, timedelta
from typing import Any

from app.core.config import settings
from app.db.session import async_session_factory
from app.worker.models import JobRecord, JobStatus
from sqlalchemy import and_, or_, select, update

logger = logging.getLogger(__name__)

JobHandler = Callable[[JobRecord], Coroutine[Any, Any, dict[str, Any] | None]]


class JobDispatcher:
    """Claim bounded attempts from the persistent jobs table (RNF003 and RNF012)."""

    def __init__(self) -> None:
        self._handlers: dict[str, JobHandler] = {}

    def register_handler(self, job_type: str, handler: JobHandler) -> None:
        """Handlers must make external side effects idempotent by job ID."""
        self._handlers[job_type] = handler

    async def fetch_and_process_next(self) -> bool:
        now = datetime.now(UTC)
        # Give the attempt time to cancel and record its outcome before recovery.
        stale_before = now - timedelta(seconds=2 * settings.JOB_TIMEOUT_SECONDS)
        async with async_session_factory.begin() as session:
            query = (
                select(JobRecord)
                .where(
                    or_(
                        JobRecord.status == JobStatus.QUEUED,
                        and_(
                            JobRecord.status == JobStatus.PROCESSING,
                            or_(
                                JobRecord.started_at.is_(None),
                                JobRecord.started_at <= stale_before,
                            ),
                        ),
                    )
                )
                .order_by(JobRecord.priority.desc(), JobRecord.created_at, JobRecord.id)
                .limit(1)
                .with_for_update(skip_locked=True)
            )
            job = (await session.execute(query)).scalar_one_or_none()
            if job is None:
                return False
            if job.status == JobStatus.PROCESSING:
                job.retry_count += 1
                job.error_message = "Previous attempt interrupted"
                if job.retry_count >= job.max_retries:
                    job.status = JobStatus.FAILED
                    return True
            job.status = JobStatus.PROCESSING
            job.started_at = now

        handler = self._handlers.get(job.job_type)
        if handler is None:
            await self._finish(
                job, status=JobStatus.FAILED, error_message="No handler registered"
            )
            return True

        try:
            async with asyncio.timeout(settings.JOB_TIMEOUT_SECONDS):
                result = await handler(job)
        except Exception as exc:
            # Provider exceptions may contain requests, credentials or private URLs.
            logger.warning("Job %s failed (%s)", job.id, type(exc).__name__)
            failures = job.retry_count + 1
            await self._finish(
                job,
                status=JobStatus.QUEUED
                if failures < job.max_retries
                else JobStatus.FAILED,
                error_message="Processing failed",
                retry_count=failures,
            )
        else:
            await self._finish(
                job,
                status=JobStatus.COMPLETED,
                error_message=None,
                result=result or {},
                completed_at=datetime.now(UTC),
            )
        return True

    async def _finish(self, job: JobRecord, **values: Any) -> None:
        # Only the attempt that currently owns the row may publish a result.
        async with async_session_factory.begin() as session:
            await session.execute(
                update(JobRecord)
                .where(
                    JobRecord.id == job.id,
                    JobRecord.status == JobStatus.PROCESSING,
                    JobRecord.started_at == job.started_at,
                )
                .values(**values)
            )


dispatcher = JobDispatcher()
