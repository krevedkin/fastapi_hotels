from datetime import date

from sqlalchemy import Computed, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Bookings(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[date] = mapped_column(Date, nullable=False)
    date_to: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    total_cost: Mapped[int] = mapped_column(
        Integer, Computed("(date_to - date_from) * price")
    )
    total_days: Mapped[int] = mapped_column(Integer, Computed("date_to - date_from"))

    first_name: Mapped[str] = mapped_column(String, nullable=True)
    second_name: Mapped[str] = mapped_column(String, nullable=True)
    phone: Mapped[int] = mapped_column(String(11), nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=False)

    room = relationship("Rooms", back_populates="booked_room")
    user = relationship("Users", back_populates="user_booking")
    

    def __str__(self) -> str:
        return f"Bookings {self.date_from} - {self.date_to}"
