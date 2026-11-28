import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_openapi_schema_contract(async_client: AsyncClient):
    response = await async_client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["openapi"].startswith("3.")
    assert "Atlas Santos" in schema["info"]["title"]
    assert "/health" in schema["paths"]
    assert "/api/v1/health" in schema["paths"]
    assert "/api/v1/auth/login" in schema["paths"]
    assert "/api/v1/photos" in schema["paths"]
    assert "/api/v1/routes" in schema["paths"]
    assert "/api/v1/exports/geojson" in schema["paths"]
