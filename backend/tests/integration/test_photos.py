from io import BytesIO

from app.core.config import settings
from app.modules.auth.seed import seed_accounts
from httpx import AsyncClient
from PIL import Image


async def test_submission_curation_and_removal(
    async_client: AsyncClient, db_session, monkeypatch
):
    await seed_accounts(db_session)
    monkeypatch.setattr(settings, "COOKIE_SECURE", False)
    async_client.headers["X-Atlas-Request"] = "1"
    photos = "/api/v1/photos"
    login = "/api/v1/auth/login"
    student = {"email": "ana@atlas.test", "password": "Santos2026!"}
    captain = {"email": "marina@atlas.test", "password": "Santos2026!"}
    assert (await async_client.post(login, json=student)).status_code == 200

    image = BytesIO()
    Image.new("RGB", (8, 8)).save(image, format="JPEG")
    submitted = await async_client.post(
        photos, files={"file": ("orla.jpg", image.getvalue(), "image/jpeg")}
    )
    assert submitted.status_code == 200
    assert submitted.json()["status"] == "pending"
    photo_id = submitted.json()["id"]
    assert (await async_client.get(photos)).json() == []

    assert (await async_client.post(login, json=captain)).status_code == 200
    queue = await async_client.get(f"{photos}/curation/queue")
    assert [photo["id"] for photo in queue.json()] == [photo_id]
    approved = await async_client.post(f"{photos}/{photo_id}/approve")
    assert approved.json()["status"] == "approved"
    assert [photo["id"] for photo in (await async_client.get(photos)).json()] == [
        photo_id
    ]

    assert (await async_client.post(login, json=student)).status_code == 200
    edited = await async_client.patch(f"{photos}/{photo_id}", json={"caption": "Orla"})
    assert edited.json()["status"] == "pending"
    assert (await async_client.delete(f"{photos}/{photo_id}")).status_code == 200
    assert (await async_client.get(f"{photos}/{photo_id}/image")).status_code == 404
