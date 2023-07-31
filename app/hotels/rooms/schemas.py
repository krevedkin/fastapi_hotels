from pydantic import BaseModel


class HotelRoomsSchema(BaseModel):
    hotel_id: int
    room_id: int
    name: str
    description: str | None
    services: list
    price: int
    quantity: int
    image_url: str
    total_price: int


class RoomSchema(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list[str]
    quantity: int
    image_url: str
