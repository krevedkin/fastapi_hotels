import typing
from datetime import date

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms

if typing.TYPE_CHECKING:
    from typing import Sequence

    from sqlalchemy import RowMapping


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def get_hotel_rooms(
        cls, hotel_id: int, date_from: date, date_to: date
    ) -> "Sequence[RowMapping]":
        async with async_session_maker() as session:
            session: AsyncSession

            days = (date_to - date_from).days

            query = (
                select(
                    Rooms.id.label("room_id"),
                    Hotels.id.label("hotel_id"),
                    Hotels.name,
                    Rooms.description,
                    Rooms.services,
                    Rooms.price,
                    Rooms.quantity,
                    Rooms.image_url,
                    (Rooms.quantity - func.count(Bookings.room_id)).label("rooms_left"),
                    (Rooms.price * days).label("total_price"),
                )
                .join(Rooms, Rooms.hotel_id == Hotels.id)
                .join(
                    Bookings,
                    and_(
                        Bookings.room_id == Rooms.id,
                        or_(
                            and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_from <= date_to,
                            ),
                            and_(
                                Bookings.date_from <= date_from,
                                Bookings.date_to > date_to,
                            ),
                        ),
                    ),
                    isouter=True,
                )
                .where(Hotels.id == hotel_id)
                .group_by(
                    Rooms.id,
                    Hotels.id,
                    Hotels.name,
                    Rooms.description,
                    Rooms.price,
                    Rooms.quantity,
                    Rooms.image_url,
                )
            )

            result = await session.execute(query)
            return result.mappings().all()
