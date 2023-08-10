from typing import Any

from sqlalchemy import (
    JSON,
    CheckConstraint,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class HotelsUsers(Base):
    __tablename__ = "hotels_users_favorite"
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user = relationship("Users", back_populates="user_favorite")
    hotel = relationship("Hotels", back_populates="user_favorite")

    __table_args__ = (
        CheckConstraint(hotel_id >= 1, name="check_min_stars"),
        UniqueConstraint(hotel_id, user_id),
    )

    def __str__(self) -> str:
        return f"HotelsUsers {self.id}"


class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)
    services: Mapped[dict[Any, Any]] = mapped_column(JSON)
    rooms_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    stars: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)

    user_favorite = relationship("HotelsUsers", back_populates="hotel")
    rooms = relationship("Rooms", back_populates="hotel")

    __table_args__ = (
        CheckConstraint(stars >= 1, name="check_min_stars"),
        CheckConstraint(stars <= 5, name="check_max_stars"),
    )

    def __str__(self) -> str:
        return f"Hotel({self.name})"
