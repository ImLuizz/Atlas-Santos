from datetime import UTC, datetime, timedelta

import pytest
from app.core.config import settings
from app.worker.dispatcher import JobDispatcher
from app.worker.models import JobRecord, JobStatus
from sqlalchemy import update
from sqlalchemy.ext.asyncio import async_sessionmaker


@pytest.fixture
def queue(db_session, monkeypatch):
    sessions = async_sessionmaker(db_session.bind, expire_on_commit=False)
    monkeypatch.setattr("app.worker.dispatcher.async_session_factory", sessions)
    return JobDispatcher()


async def test_retry_uses_same_job_id_and_hides_provider_error(queue, db_session):
    job = JobRecord(job_type="test")
    db_session.add(job)
    await db_session.commit()
    calls = []

    async def handler(record):
        calls.append(record.id)
        if len(calls) == 1:
            raise RuntimeError("provider returned private content")
        return {"done": True}

    queue.register_handler("test", handler)
    assert await queue.fetch_and_process_next()
    await db_session.refresh(job)
    assert job.status == JobStatus.QUEUED and job.retry_count == 1
    assert "private content" not in job.error_message
    assert await queue.fetch_and_process_next()
    await db_session.refresh(job)
    assert calls == [job.id, job.id]
    assert job.status == JobStatus.COMPLETED and job.result == {"done": True}
    assert job.error_message is None
    assert not await queue.fetch_and_process_next()


async def test_only_abandoned_attempt_is_recovered(queue, db_session):
    now = datetime.now(UTC)
    old = now - timedelta(seconds=3 * settings.JOB_TIMEOUT_SECONDS)
    abandoned = JobRecord(job_type="test", status=JobStatus.PROCESSING, started_at=old)
    active = JobRecord(job_type="test", status=JobStatus.PROCESSING, started_at=now)
    db_session.add_all([abandoned, active])
    await db_session.commit()

    async def handler(record):
        assert record.id == abandoned.id
        return {"retried": True}

    queue.register_handler("test", handler)
    assert await queue.fetch_and_process_next()
    assert not await queue.fetch_and_process_next()
    await db_session.refresh(abandoned)
    assert abandoned.status == JobStatus.COMPLETED
    assert abandoned.retry_count == 1


async def test_late_worker_cannot_overwrite_new_attempt(queue, db_session):
    job = JobRecord(job_type="test")
    db_session.add(job)
    await db_session.commit()

    async def late_handler(record):
        await db_session.execute(
            update(JobRecord)
            .where(JobRecord.id == record.id)
            .values(started_at=record.started_at + timedelta(minutes=10))
        )
        await db_session.commit()
        return {"late": True}

    queue.register_handler("test", late_handler)
    assert await queue.fetch_and_process_next()
    await db_session.refresh(job)
    assert job.status == JobStatus.PROCESSING
    assert job.result is None


async def test_unregistered_handler_fails_without_result(queue, db_session):
    job = JobRecord(job_type="unimplemented")
    db_session.add(job)
    await db_session.commit()
    assert await queue.fetch_and_process_next()
    await db_session.refresh(job)
    assert job.status == JobStatus.FAILED
    assert job.result is None and job.completed_at is None
