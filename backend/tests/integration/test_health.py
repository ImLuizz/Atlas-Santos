import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root_health_endpoint(async_client: AsyncClient):
    response = await async_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["app_name"] == "Atlas Santos API"
    assert "version" in data
    assert "timestamp" in data
    assert data["database"] == "connected"


@pytest.mark.asyncio
async def test_api_v1_health_endpoint(async_client: AsyncClient):
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["environment"] == "test"


@pytest.mark.asyncio
async def test_database_unavailable(async_client: AsyncClient, monkeypatch):
    async def unavailable(session):
        return False

    monkeypatch.setattr("app.api.v1.endpoints.health.check_db_connection", unavailable)
    response = await async_client.get("/health")
    assert response.status_code == 503
    assert response.json()["database"] == "disconnected"
