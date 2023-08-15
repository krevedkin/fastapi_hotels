from datetime import date

from sqlalchemy import and_, case, delete, func, insert, or_, select
from sqlalchemy.exc import IntegrityError

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.exceptions import FavoriteHotelAlreadyExistsDBexception
from app.hotels.models import Hotels, HotelsUsers
from app.hotels.rooms.models import Rooms


class HotelsDAO(BaseDAO):
    model = Hotels

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
        user_id: int,
        city: str | None = None,
        stars: int | None = None,
        min_price: int | None = None,
        max_price: int | None = None,
        favorites_only: bool | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ):
        """Запрос на получения отелей с фильтрацией
        В зависимости от переданных параметров возвращает список отелей,
        Если какой то параметр является None то он не участвует в фильтрации.

        При переданных date_to и date_from возвращает список отелей у которых
        на этот период дат есть хотя бы одна не забронированная комната

        для наглядности полный SQL запрос со всеми фильтрами выглядит так:

        SELECT hotels.id,
            DISTINCT(hotels.name),
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
                 WHERE (
                        bookings.date_from >= :date_from
                        AND bookings.date_from <= :date_to
                                )
                        OR (
                            bookings.date_from <= :date_from
                            AND bookings.date_to >= :date_from
                                )
                        )
        GROUP BY hotels.id, hotels_users_favorite.id

        Returns:
            Coroutine[Any, Any, Sequence[RowMapping]] : Список отелей
            удовлетворяющих условиям фильтрации, либо все что есть
        """
        async with async_session_maker() as session:
            filters = []
            if city:
                filters.append(func.lower(Hotels.city) == city.lower())
            if stars and stars in range(1, 6):
                filters.append(Hotels.stars == stars)
            if min_price and max_price:
                filters.append(and_(Rooms.price.between(min_price, max_price)))
            if favorites_only:
                filters.append(
                    HotelsUsers.id.isnot(None) if True else HotelsUsers.id.is_(None),
                )
                filters.append(HotelsUsers.user_id == user_id)

            if date_from and date_to:
                bookings_query = (
                    select(func.count(Bookings.id))
                    .outerjoin(Rooms)
                    .join(Hotels)
                    .where(
                        or_(
                            and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_from <= date_to,
                            ),
                            and_(
                                Bookings.date_from <= date_from,
                                Bookings.date_to >= date_from,
                            ),
                        )
                    )
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
                    func.distinct(Hotels.id).label("id"),
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
