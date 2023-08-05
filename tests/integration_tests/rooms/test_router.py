import pytest

from httpx import AsyncClient


@pytest.mark.rooms
async def test_get_room(auth_ac: AsyncClient):
    response = await auth_ac.get("/hotels/rooms/1")
    assert response.status_code == 200

    room_fields = (
        "id",
        "hotel_id",
        "name",
        "description",
        "price",
        "services",
        "quantity",
        "image_url",
    )
    room = response.json()

    for field in room_fields:
        assert field in room


@pytest.mark.rooms
async def test_get_room_that_does_not_exist(auth_ac: AsyncClient):
    response = await auth_ac.get("/hotels/rooms/1000")
    assert response.status_code == 404
    assert response.json()["detail"] == "Записи не существует"
