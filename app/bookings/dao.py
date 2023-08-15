from datetime import date

from sqlalchemy import and_, delete, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


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
        """
        Метод для добавления нового бронирования.
        Если на выбранный период дат нет свободных номеров бронирование
        не будет осуществлено.

        Args:
            date_from (date): Дата въезда
            date_to (date): Дата выезда
            room_id (int): Индентификатор комнаты
            user_id (int): Индентификатор пользователя
            email (str): Email пользователя
            first_name (str | None): Имя пользователя
            second_name (str | None): Фамилия пользователя
            phone (str | None): Телефон пользователя

        Returns:
            Booking - Объект бронирования в случае успешного бронирования
            None - В случае если все комнаты заняты и бронирование не удалось

        Для наглядности пример SQL запроса
                WITH booked_rooms AS (
            SELECT bookings.id AS id,
                bookings.room_id AS room_id,
                bookings.user_id AS user_id,
                bookings.date_from AS date_from,
                bookings.date_to AS date_to,
                bookings.price AS price,
                bookings.total_cost AS total_cost,
                bookings.total_days AS total_days,
                bookings.first_name AS first_name,
                bookings.second_name AS second_name,
                bookings.phone AS phone,
                bookings.email AS email
            FROM bookings
            WHERE bookings.room_id = :room_id_1
                AND (
                    bookings.date_from >= :date_from_1
                    AND bookings.date_from <= :date_from_2
                    OR bookings.date_from <= :date_from_3
                    AND bookings.date_to > :date_to_1
                )
        )
        SELECT rooms.quantity - count(booked_rooms.room_id) AS rooms_left,
            rooms.price
        FROM rooms
            LEFT OUTER JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = :id_1
        GROUP BY rooms.quantity,
            rooms.price


        """
        async with async_session_maker() as session:
            booked_rooms = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.room_id == room_id,
                        or_(
                            and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_from <= date_to,
                            ),
                            and_(
                                Bookings.date_from <= date_from,
                                Bookings.date_to > date_from,
                            ),
                        ),
                    )
                )
                .cte("booked_rooms")
            )

            get_rooms_left = (
                select(
                    (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                        "rooms_left"
                    ),
                    Rooms.price,
                )
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.id == room_id)
                .group_by(Rooms.quantity, Rooms.price)
            )

            rooms_left = await session.execute(get_rooms_left)
            rooms_left, room_price = rooms_left.mappings().one().values()

            if rooms_left > 0:
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
