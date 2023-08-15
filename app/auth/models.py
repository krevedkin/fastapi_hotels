from datetime import datetime
from typing import Literal

from sqlalchemy import DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[Literal["user", "admin"]] = mapped_column(
        String, default="user", nullable=True
    )

    user_favorite = relationship("HotelsUsers", back_populates="user")
    user_booking = relationship("Bookings", back_populates="user")

    def __str__(self) -> str:
        return f"Users({self.email})"


class RefreshSessions(Base):
    __tablename__ = "refresh_sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    refresh_token: Mapped[Uuid] = mapped_column(Uuid, unique=True)
    expire: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    expire: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
