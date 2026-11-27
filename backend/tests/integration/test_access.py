from datetime import UTC, datetime, timedelta

import pytest
from app.core.config import settings
from app.core.security import hash_token
from app.modules.auth.models import Session, User
from app.modules.auth.seed import seed_accounts
from app.modules.teams.models import Team
from sqlalchemy import func, select

AUTH = "/api/v1/auth"
HEADERS = {"X-Atlas-Request": "1"}


@pytest.fixture
async def accounts(db_session, monkeypatch):
    monkeypatch.setattr(settings, "COOKIE_SECURE", False)
    await seed_accounts(db_session)


async def login(client, email, password="Santos2026!"):
    return await client.post(
        f"{AUTH}/login", headers=HEADERS, json={"email": email, "password": password}
    )


@pytest.mark.parametrize(
    ("email", "kind", "role", "team"),
    [
        ("ana@atlas.test", "estudante", "participante", "Centro"),
        ("marina@atlas.test", "estudante", "capitao", "Centro"),
        ("caio@atlas.test", "servidor", "participante", "Orla"),
    ],
)
async def test_identity_session_and_logout(
    accounts, async_client, db_session, email, kind, role, team
):
    client = async_client
    assert (await client.get(f"{AUTH}/me")).status_code == 401
    entered = await login(client, email.upper())
    assert entered.status_code == 200
    user = entered.json()
    assert (user["participant_kind"], user["role"], user["team"]["name"]) == (
        kind,
        role,
        team,
    )
    assert user["team"]["atlas_name"] == f"Atlas da equipe {team}"
    assert user["photo_quota"] == 20
    token = client.cookies["atlas_session"]
    assert "httponly" in entered.headers["set-cookie"].lower()
    assert "samesite=lax" in entered.headers["set-cookie"].lower()
    assert "no-store" in entered.headers["cache-control"]
    assert token not in entered.text
    assert "password_hash" not in user
    assert (await db_session.scalar(select(Session.token_hash))) == hash_token(token)
    assert (await client.get(f"{AUTH}/me")).json() == user
    assert (await client.post(f"{AUTH}/logout")).status_code == 403
    assert (await client.post(f"{AUTH}/logout", headers=HEADERS)).status_code == 200
    assert not client.cookies
    client.cookies.set("atlas_session", token)
    assert (await client.get(f"{AUTH}/me")).status_code == 401


async def test_captain_can_only_view_own_team(accounts, async_client, db_session):
    centro = await db_session.scalar(select(Team.id).where(Team.name == "Centro"))
    orla = await db_session.scalar(select(Team.id).where(Team.name == "Orla"))
    path = f"/api/v1/teams/{centro}/members"
    assert (await async_client.get(path)).status_code == 401
    for email in ["ana@atlas.test", "caio@atlas.test"]:
        user = (await login(async_client, email)).json()
        response = await async_client.get(f"/api/v1/teams/{user['team']['id']}/members")
        assert response.status_code == 403
    await login(async_client, "marina@atlas.test")
    assert [u["name"] for u in (await async_client.get(path)).json()] == [
        "Ana Souza",
        "Marina Costa",
    ]
    assert (await async_client.get(f"/api/v1/teams/{orla}/members")).status_code == 403


async def test_production_rejects_existing_fictitious_sessions(
    accounts, async_client, db_session, monkeypatch
):
    assert (await login(async_client, "ana@atlas.test")).status_code == 200
    monkeypatch.setattr(settings, "ENVIRONMENT", "production")
    assert (await async_client.get(f"{AUTH}/me")).status_code == 401
    assert (await login(async_client, "ana@atlas.test")).status_code == 401
    user = await db_session.scalar(select(User).where(User.email == "ana@atlas.test"))
    user.email = "ana@example.org"
    await db_session.commit()
    assert (await login(async_client, user.email)).status_code == 200


async def test_failed_login_leaves_no_accounts_or_sessions(async_client, db_session):
    assert (await login(async_client, "ana@atlas.test")).status_code == 401
    assert not await db_session.scalar(select(User.id))
    assert not await db_session.scalar(select(Session.id))


async def test_wrong_password_validation_and_request_header(accounts, async_client):
    credentials = {"email": "ana@atlas.test", "password": "Santos2026!"}
    assert (
        await async_client.post(f"{AUTH}/login", json=credentials)
    ).status_code == 403
    assert (
        await login(async_client, credentials["email"], "errada")
    ).status_code == 401
    invalid = await login(async_client, credentials["email"], "secret" * 40)
    assert invalid.status_code == 422
    assert "secret" not in invalid.text


async def test_suspended_account_and_expired_session(
    accounts, async_client, db_session
):
    await login(async_client, "ana@atlas.test")
    session = await db_session.scalar(select(Session))
    session.expires_at = datetime.now(UTC) - timedelta(seconds=1)
    await db_session.commit()
    assert (await async_client.get(f"{AUTH}/me")).status_code == 401
    await login(async_client, "ana@atlas.test")
    user = await db_session.get(User, session.user_id)
    user.active = False
    await db_session.commit()
    assert (await async_client.get(f"{AUTH}/me")).status_code == 401
    assert (await login(async_client, user.email)).status_code == 401


async def test_seed_preserves_accounts_and_rejects_production(
    accounts, db_session, monkeypatch
):
    original = await db_session.scalar(
        select(User).where(User.email == "ana@atlas.test")
    )
    original.password_hash = "already-changed"
    await db_session.commit()
    await seed_accounts(db_session)
    assert await db_session.scalar(select(func.count()).select_from(User)) == 3
    await db_session.refresh(original)
    assert original.password_hash == "already-changed"
    monkeypatch.setattr(settings, "ENVIRONMENT", "production")
    with pytest.raises(RuntimeError, match="exclusivo"):
        await seed_accounts(db_session)
    monkeypatch.setattr(settings, "ENVIRONMENT", "staging")
    monkeypatch.delenv("ATLAS_TEST_ACCOUNT_PASSWORD", raising=False)
    with pytest.raises(RuntimeError, match="ATLAS_TEST_ACCOUNT_PASSWORD"):
        await seed_accounts(db_session)
