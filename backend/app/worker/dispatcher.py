import logging
from collections.abc import Callable, Coroutine
from datetime import UTC, datetime
from typing import Any

from app.db.base import JobRecord, JobStatus
from app.db.session import async_session_factory
from sqlalchemy import select, update

logger = logging.getLogger(__name__)

# Type alias for async job handler functions
JobHandler = Callable[[JobRecord], Coroutine[Any, Any, dict[str, Any] | None]]


class JobDispatcher:
    """
    Coordinates asynchronous task execution from the persistent jobs table.
    Enforces transactional consistency and isolation (RNF-06).
    """

    def __init__(self) -> None:
        self._handlers: dict[str, JobHandler] = {}

    def register_handler(self, job_type: str, handler: JobHandler) -> None:
        """Register a processing routine for a given job type."""
        self._handlers[job_type] = handler
        logger.info(f"Registered worker handler for job type: '{job_type}'")

    async def fetch_and_process_next(self) -> bool:
        """
        Polls the database for the next queued job, executes it, and updates its state.
        Returns True if a job was found and processed, False otherwise.
        """
        async with async_session_factory() as session:
            # Atomic fetch-and-lock of highest-priority queued job
            query = (
                select(JobRecord)
                .where(JobRecord.status == JobStatus.QUEUED)
                .order_by(JobRecord.priority.desc(), JobRecord.created_at.asc())
                .limit(1)
                .with_for_update(skip_locked=True)
            )
            result = await session.execute(query)
            job = result.scalar_one_or_none()

            if not job:
                return False

            # Mark as processing
            job.status = JobStatus.PROCESSING
            job.started_at = datetime.now(UTC)
            await session.commit()
            job_id = job.id
            job_type = job.job_type

        # Dispatch job outside the initial lock transaction
        handler = self._handlers.get(job_type)
        if not handler:
            logger.error(f"No handler registered for job {job_id} of type '{job_type}'")
            await self._mark_failed(job_id, f"No handler registered for '{job_type}'")
            return True

        try:
            logger.info(f"Executing job {job_id} [{job_type}]")
            output = await handler(job)
            await self._mark_completed(job_id, output)
            return True
        except Exception as exc:
            logger.exception(f"Job {job_id} failed with error: {exc}")
            await self._mark_failed(job_id, str(exc))
            return True

    async def _mark_completed(self, job_id: str, result: dict[str, Any] | None) -> None:
        async with async_session_factory() as session:
            await session.execute(
                update(JobRecord)
                .where(JobRecord.id == job_id)
                .values(
                    status=JobStatus.COMPLETED,
                    result=result or {},
                    completed_at=datetime.now(UTC),
                )
            )
            await session.commit()

    async def _mark_failed(self, job_id: str, error_message: str) -> None:
        async with async_session_factory() as session:
            # Check retry count
            stmt = select(JobRecord).where(JobRecord.id == job_id)
            res = await session.execute(stmt)
            job = res.scalar_one_or_none()
            if job:
                job.retry_count += 1
                if job.retry_count < job.max_retries:
                    job.status = JobStatus.QUEUED  # Retry
                else:
                    job.status = JobStatus.FAILED
                job.error_message = error_message
                await session.commit()


dispatcher = JobDispatcher()
