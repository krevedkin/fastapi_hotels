from sqladmin import ModelView

from app.auth.models import Users
from app.bookings.models import Bookings
from app.hotels.models import Hotels, HotelsUsers
from app.hotels.rooms.models import Rooms


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email, Users.user_booking]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c for c in Bookings.__table__.columns] + [
        Bookings.room,
        Bookings.user,
    ]  # type: ignore
    name = "Бронирование"
    name_plural = "Бронирования"
    icon = "fa-solid fa-book"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c for c in Hotels.__table__.columns] + [Hotels.rooms]  # type: ignore
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"


class HotelsUsersAdmin(ModelView, model=HotelsUsers):
    column_list = [c for c in HotelsUsers.__table__.columns] + [
        HotelsUsers.user,
        HotelsUsers.hotel,
    ]  # type: ignore
    name = "Избранный отель пользователя"
    name_plural = "Избранные отели пользователя"
    icon = "fa-solid fa-heart"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c for c in Rooms.__table__.columns] + [Rooms.hotel]  # type: ignore
    name = "Комната"
    name_plural = "Комнаты"
    icon = "fa-solid fa-bed"
