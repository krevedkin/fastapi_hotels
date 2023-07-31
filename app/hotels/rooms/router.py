from datetime import date

from app.hotels.rooms.schemas import HotelRoomsSchema
from app.hotels.router import router
from app.hotels.rooms.dao import RoomsDAO


@router.get("/{hotel_id}/rooms")
async def get_hotel_rooms(
    hotel_id: int, date_from: date, date_to: date
) -> list[HotelRoomsSchema]:
    return await RoomsDAO.get_hotel_rooms(hotel_id, date_from, date_to)


@router.get("/rooms/{room_id}")
async def get_room(room_id: int):
    return await RoomsDAO.get_by_id(room_id)
