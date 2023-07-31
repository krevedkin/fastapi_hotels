from datetime import date
from typing import Any
from sqlalchemy import case, insert, select, func, or_, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.dao.base import BaseDAO
from app.hotels.models import Hotels, HotelsUsers
from app.database import async_session_maker
from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.hotels.exceptions import FavoriteHotelAlreadyExistsDBexception


class HotelsDAO(BaseDAO):
    model = Hotels

    # @classmethod
    # async def get_hotels_by_location(cls, location: str, date_from, date_to):
    #     async with async_session_maker() as session:
    #         session: AsyncSession
    #         booked_rooms_count = (
    #             select(func.count().label("booked_rooms_count"))
    #             .select_from(Bookings)
    #             .where(
    #                 or_(
    #                     and_(
    #                         Bookings.date_from >= date_from,
    #                         Bookings.date_from <= date_to,
    #                     ),
    #                     and_(
    #                         Bookings.date_from <= date_from,
    #                         Bookings.date_from > date_to,
    #                     ),
    #                 )
    #             )
    #         ).as_scalar()

    #         query = (
    #             select(
    #                 Hotels.id,
    #                 Hotels.name,
    #                 Hotels.location,
    #                 Hotels.rooms_quantity,
    #                 Hotels.services,
    #                 Hotels.image_url,
    #                 (Hotels.rooms_quantity - func.count(Bookings.room_id)).label(
    #                     "rooms_left"
    #                 ),
    #             )
    #             .join(Rooms, Hotels.id == Rooms.hotel_id)
    #             .join(Bookings, Rooms.id == Bookings.room_id, isouter=True)
    #             .where(
    #                 and_(
    #                     Hotels.location.ilike(f"%{location}%"),
    #                     # type: ignore
    #                     Hotels.rooms_quantity > booked_rooms_count,
    #                 )
    #             )
    #             .group_by(
    #                 Hotels.id,
    #                 Hotels.name,
    #                 Hotels.location,
    #                 Hotels.rooms_quantity,
    #                 Hotels.image_url,
    #             )
    #             .having(Hotels.rooms_quantity - func.count(Bookings.room_id) > 0)
    #         )

    #     result = await session.execute(query)
    #     return result.mappings().all()

    # @classmethod
    # async def get_hotels(cls):
    #     async with async_session_maker() as session:
    #         query = select(
    #             Hotels.id,
    #             Hotels.name,
    #             Hotels.location,
    #             Hotels.image_url,
    #             Hotels.stars,
    #             Hotels.description,
    #         )
    #         result = await session.execute(query)
    #         return result.mappings().all()

    @classmethod
    async def _build_query(cls, date_from, date_to):
        async with async_session_maker() as session:
            booked_rooms_count = (
                select(func.count().label("booked_rooms_count"))
                .select_from(Bookings)
                .where(
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to,
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_from > date_to,
                        ),
                    )
                )
            )
            # r = await session.execute(booked_rooms_count)
            # print(r.mappings().all())
            print(booked_rooms_count)
            # return booked_rooms_count

    @classmethod
    async def get_hotel_with_rooms(cls, hotel_id: int):
        async with async_session_maker() as session:
            hotel_query = select(Hotels.__table__).where(Hotels.id == hotel_id)
            rooms_query = select(Rooms.__table__).where(Rooms.hotel_id == hotel_id)
            hotels = await session.execute(hotel_query)
            rooms = await session.execute(rooms_query)

            hotels = hotels.mappings().one_or_none()  # type:ignore

            if not hotels:
                return None

            hotels = dict(hotels)
            rooms = rooms.mappings().all()
            hotels["rooms"] = [dict(room) for room in rooms]  # type:ignore

            return hotels

    @classmethod
    async def get_hotels(
        cls,
        city: str | None,
        stars: int | None,
        min_price: int | None,
        max_price: int | None,
        favorites_only: bool | None,
        date_from: date | None,
        date_to: date | None,
    ):
        """Запрос на получения отелей с фильтрацией
        В зависимости от переданных параметров возвращает список отелей,
        Если какой то параметр является None то он не участвует в фильтрации.

        При переданных date_to и date_from возвращает список отелей у которых
        на этот период дат есть хотя бы одна не забронированная комната

        для наглядности полный SQL запрос со всеми фильтрами выглядит так:

        SELECT hotels.id,
            hotels.name,
            hotels.description,
            hotels.stars,
            hotels.city,
            hotels.image_url,
            min(rooms.price) AS min_price,
            CASE
                WHEN (hotels_users_favorite.id IS NOT NULL) THEN True
                ELSE False
            END AS is_favorite
        FROM hotels
            JOIN rooms ON hotels.id = rooms.hotel_id
            LEFT OUTER JOIN hotels_users_favorite ON hotels.id =
                                hotels_users_favorite.hotel_id
        WHERE hotels.city = :city_1
            AND hotels.stars = :stars_1
            AND rooms.price BETWEEN :price_1 AND :price_2
            AND hotels.rooms_quantity > (
                SELECT count(bookings.id) AS count_1
                FROM bookings
                    LEFT OUTER JOIN rooms ON rooms.id =
                                        bookings.room_id
                    JOIN hotels ON hotels.id = rooms.hotel_id
                WHERE bookings.date_from BETWEEN :date_from_1
                                            AND :date_from_2
            )
        GROUP BY hotels.id, hotels_users_favorite.id

        Returns:
            Coroutine[Any, Any, Sequence[RowMapping]] : Список отелей
            удовлетворяющих условиям фильтрации, либо все что есть
        """
        async with async_session_maker() as session:
            filters = []
            if city:
                filters.append(Hotels.city == city)
            if stars:
                filters.append(Hotels.stars == stars)
            filters.append(and_(Rooms.price.between(min_price, max_price)))

            if favorites_only:
                filters.append(
                    HotelsUsers.id.isnot(None) if True else HotelsUsers.id.is_(None)
                )

            if date_from and date_to:
                bookings_query = (
                    select(func.count(Bookings.id))
                    .outerjoin(Rooms)
                    .join(Hotels)
                    .where(Bookings.date_from.between(date_from, date_to))
                )
                filters.append(and_(Hotels.rooms_quantity > bookings_query))

            is_favorite = case(
                (
                    HotelsUsers.id.isnot(None),
                    True,
                ),
                else_=False,
            ).label("is_favorite")

            query = (
                select(
                    Hotels.id,
                    Hotels.name,
                    Hotels.description,
                    Hotels.stars,
                    Hotels.city,
                    Hotels.image_url,
                    func.min(Rooms.price).label("min_price"),
                    is_favorite,
                )
                .join(Rooms)
                .outerjoin(HotelsUsers)
                .group_by(Hotels.id, HotelsUsers.id)
                .filter(and_(*filters))
            )

            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def get_locations(cls):
        async with async_session_maker() as session:
            query = select(func.distinct(Hotels.city))
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add_favorite_hotel(cls, user_id: int, hotel_id: int):
        async with async_session_maker() as session:
            stmt = (
                insert(HotelsUsers)
                .values(user_id=user_id, hotel_id=hotel_id)
                .returning(HotelsUsers.id)
            )
            try:
                result = await session.execute(stmt)
                await session.commit()
            except IntegrityError:
                raise FavoriteHotelAlreadyExistsDBexception

            return result.mappings().first()

    @classmethod
    async def delete_favorite_hotel(cls, user_id: int, hotel_id: int) -> bool:
        async with async_session_maker() as session:
            stmt = delete(HotelsUsers).where(
                and_(
                    HotelsUsers.hotel_id == hotel_id,
                    HotelsUsers.user_id == user_id,
                )
            )
            result = await session.execute(stmt)

            if result.rowcount != 0:  # type: ignore
                await session.commit()
                return True
            else:
                return False

    @classmethod
    async def test_request(cls):
        async with async_session_maker() as session:
            query = select(Hotels.id.label("lolkek"))
            result = await session.execute(query)
            return result.mappings().all()
