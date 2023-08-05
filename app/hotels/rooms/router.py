from app.hotels.rooms.dao import RoomsDAO
from app.hotels.router import router


@router.get("/rooms/{room_id}")
async def get_room(room_id: int):
    return await RoomsDAO.get_by_id(room_id)
