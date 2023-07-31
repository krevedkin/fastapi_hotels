import asyncio
from datetime import datetime
import json
import pytest
from sqlalchemy import insert
from httpx import AsyncClient

from app.main import app as fastapi_app
from app.database import Base, async_session_maker, engine
from app.config import settings
from app.bookings.models import Bookings
from app.auth.models import Users
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    assert settings.MODE == "TEST"
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"tests/mock_data/mock_{model}.json") as f:
            return json.load(f)

    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(
            booking["date_from"],
            "%Y-%m-%d",
        )
        booking["date_to"] = datetime.strptime(
            booking["date_to"],
            "%Y-%m-%d",
        )

    async with async_session_maker() as session:
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_users = insert(Users).values(users)
        add_bookings = insert(Bookings).values(bookings)

        for stmt in (add_hotels, add_rooms, add_users, add_bookings):
            await session.execute(stmt)
            await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    """
    Взято из документации pytest
    Create an instance of the default event loop
    for each test case
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function")
async def auth_ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
        response = await client.post(
            "/auth/token",
            data={
                "username": "user@example.com",
                "password": "string",
            },
        )

        token = response.json().get("access_token")
        client.headers["Authorization"] = f"Bearer {token}"
        yield client
