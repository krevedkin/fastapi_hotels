from app.hotels.exceptions import RecordDoesNotExists
from app.hotels.rooms.dao import RoomsDAO
from app.hotels.router import router


@router.get("/rooms/{room_id}")
async def get_room(room_id: int):
    room = await RoomsDAO.get_by_id(room_id)
    if not room:
        raise RecordDoesNotExists
    return room
