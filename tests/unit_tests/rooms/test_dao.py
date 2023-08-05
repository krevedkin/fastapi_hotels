from datetime import date

import pytest

from app.hotels.rooms.dao import RoomsDAO


@pytest.mark.rooms
async def test_get_hotel_rooms_with_no_rooms_left():
    rooms = await RoomsDAO().get_hotel_rooms(
        hotel_id=12,
        date_from=date(2023, 5, 10),
        date_to=date(2023, 5, 20),
    )

    assert rooms[0]["rooms_left"] == 0
