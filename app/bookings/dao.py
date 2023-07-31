from datetime import date
from sqlalchemy import delete, func, insert, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings
from app.hotels.models import Hotels


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def get_bookings(cls, user_id: int):
        async with async_session_maker() as session:
            session: AsyncSession

            query = (
                select(
                    Bookings.id.label("booking_id"),
                    Bookings.room_id,
                    Bookings.user_id,
                    Bookings.date_from,
                    Bookings.date_to,
                    Bookings.price,
                    Bookings.total_cost,
                    Bookings.total_days,
                    Rooms.image_url,
                    Rooms.name.label("room_name"),
                    Rooms.description,
                    Rooms.services,
                    Hotels.name.label("hotel_name"),
                )
                .join(Rooms, Rooms.id == Bookings.room_id)
                .join(Hotels, Hotels.id == Rooms.hotel_id)
                .where(Bookings.user_id == user_id)
            )

            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def insert_record(
        cls,
        date_from: date,
        date_to: date,
        room_id: int,
        user_id: int,
        email: str,
        first_name: str | None,
        second_name: str | None,
        phone: str | None,
    ):
        async with async_session_maker() as session:
            bookings_query = (
                select(
                    (Rooms.quantity - func.count(Bookings.id)).label(
                        "free_rooms_count"
                    ),
                    Rooms.price,
                )
                .select_from(Bookings)
                .outerjoin(Rooms)
                .where(
                    and_(
                        Bookings.date_from.between(date_from, date_to),
                        Bookings.room_id == room_id,
                    )
                )
                .group_by(Rooms.quantity, Rooms.price)
            )

            result = await session.execute(bookings_query)
            result = result.mappings().one_or_none()

            if result:
                free_rooms_count, room_price = result.values()
                if free_rooms_count and free_rooms_count > 0:
                    booking = Bookings(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=room_price,
                        email=email,
                        first_name=first_name,
                        second_name=second_name,
                        phone=phone,
                    )
                    session.add(booking)
                    await session.flush()
                    await session.commit()
                    return booking
            else:
                query = select(Rooms.price).where(Rooms.id == room_id)
                result = await session.execute(query)
                room_price = result.scalar()
                booking = Bookings(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=room_price,
                    email=email,
                    first_name=first_name,
                    second_name=second_name,
                    phone=phone,
                )
                session.add(booking)
                await session.flush()
                await session.commit()
                return booking

            return None

    @classmethod
    async def delete_record(cls, booking_id: int, user_id: int):
        async with async_session_maker() as session:
            stmt = delete(cls.model).where(
                and_(
                    cls.model.id == booking_id,
                    cls.model.user_id == user_id,
                )
            )
            result = await session.execute(stmt)

            if result.rowcount != 0:  # type: ignore
                await session.commit()
                return True
            else:
                return False

    @classmethod
    async def get_bookings_count(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(func.count(Bookings.id)).where(Bookings.user_id == user_id)
            result = await session.execute(query)
            return result.scalar_one()
