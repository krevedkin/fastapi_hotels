from pydantic import BaseModel


class RoomSchema(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list[str]
    quantity: int
    image_url: str
