from pydantic import BaseModel

from app.hotels.rooms.schemas import RoomSchema


class HotelFavoriteSchema(BaseModel):
    hotel_id: int


class HotelDetailSchema(BaseModel):
    id: str
    name: str
    location: str
    services: list[str]
    rooms_quantity: str
    image_url: str
    stars: int
    description: str
    city: str
    address: str
    rooms: list[RoomSchema]


class HotelSchema(BaseModel):
    id: int
    name: str
    description: str
    stars: int
    city: str
    image_url: str
    min_price: int
    is_favorite: bool
