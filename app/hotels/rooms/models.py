from typing import Any

from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    hotel = relationship("Hotels", back_populates="rooms")
    booked_room = relationship("Bookings", back_populates="room")

    def __str__(self) -> str:
        return f"Room #{self.id} {self.name}"
