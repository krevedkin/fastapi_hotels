from sqlalchemy import String, JSON, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from typing import Any

from app.database import Base


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)
    services: Mapped[dict[str, Any]] = mapped_column(JSON)
    quantity: Mapped[int] = mapped_column(Integer)
    image_url: Mapped[str] = mapped_column(String, nullable=True)
