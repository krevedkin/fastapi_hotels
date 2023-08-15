import uuid
from datetime import datetime, timedelta, timezone

import pytest
from httpx import AsyncClient

from app.auth.dao import RefreshSessionsDAO


@pytest.mark.auth
@pytest.mark.parametrize(
    ("username", "password", "status_code"),
    [
        ("user@example.com", "string", 200),
        ("user@example.com", "wrong_password", 401),
        ("wrongemail@example.com", "string", 401),
    ],
)
async def test_login(username, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/token",
        data={
            "username": username,
            "password": password,
        },
    )

    assert response.status_code == status_code

    if response.status_code == 200:
        assert response.cookies.get("hotels-app-refresh")
        data = response.json()
        assert data.get("token_type") == "bearer"
        assert data.get("access_token")
    else:
        assert response.cookies.get("hotels-app-refresh") is None


@pytest.mark.auth
async def test_protected_endpoint(ac: AsyncClient, auth_ac: AsyncClient):
    response = await auth_ac.get("/auth/me")
    assert response.status_code == 200

    bad_response = await ac.get("/auth/me")
    assert bad_response.status_code == 401


@pytest.mark.auth
async def test_refresh(auth_ac: AsyncClient):
    old_refresh_token = auth_ac.cookies.get("hotels-app-refresh")

    response = await auth_ac.post("/auth/refresh")

    new_refresh_token = response.cookies.get("hotels-app-refresh")
    assert auth_ac.cookies.get("hotels-app-refresh") == response.cookies.get(
        "hotels-app-refresh"
    )
    assert old_refresh_token != new_refresh_token

    auth_ac.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
    response_with_new_token = await auth_ac.get("/auth/me")
    assert response_with_new_token.status_code == 200


@pytest.mark.auth
async def test_refresh_without_cookie(auth_ac: AsyncClient):
    auth_ac.cookies.delete("hotels-app-refresh")
    response = await auth_ac.post("/auth/refresh")
    assert response.status_code == 401
    assert response.json()["detail"] == "refresh token отсутствует"


@pytest.mark.auth
async def test_refresh_session_not_exists(auth_ac: AsyncClient):
    auth_ac.cookies.delete("hotels-app-refresh")
    auth_ac.cookies.set("hotels-app-refresh", str(uuid.uuid4()))
    response = await auth_ac.post("/auth/refresh")
    assert response.status_code == 401
    assert (
        response.json()["detail"]
        == "Сессия не найдена. Пройдите процедуру аутентификации заново"
    )


# TODO разобраться как делать мок
@pytest.mark.skip
async def test_refresh_token_expired(mocker, auth_ac: AsyncClient):
    refresh_session = mocker.Mock()

    refresh_session.expire = datetime.now(timezone.utc) - timedelta(minutes=10)

    mocker.patch(
        "app.auth.dao.RefreshSessionsDAO"
    ).return_value.get_refresh_session.return_value = refresh_session

    response = await auth_ac.post("/auth/refresh")

    assert response.status_code == 401


@pytest.mark.auth
async def test_logout(auth_ac: AsyncClient):
    refresh_token = auth_ac.cookies.get("hotels-app-refresh")
    await auth_ac.post("/auth/logout")
    assert auth_ac.cookies.get("hotels-app-refresh") is None

    session = await RefreshSessionsDAO.get_refresh_session(refresh_token)  # type:ignore
    assert session is None


@pytest.mark.auth
@pytest.mark.parametrize(
    ("email", "password", "status_code"),
    [
        ("first_user@example.com", "string", 201),
        ("first_user@example.com", "string", 409),
        ("lessthan5password@example.com", "12345", 422),
    ],
)
async def test_register(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/register",
        json={"email": email, "password": password},
    )

    assert response.status_code == status_code
