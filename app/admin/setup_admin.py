import typing

from sqladmin import Admin

from app.admin import views
from app.admin.auth import authentication_backend
from app.database import engine

if typing.TYPE_CHECKING:
    from fastapi import FastAPI


def setup_admin(app: "FastAPI"):
    admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)
    admin.add_view(views.UsersAdmin)
    admin.add_view(views.HotelsUsersAdmin)
    admin.add_view(views.BookingsAdmin)
    admin.add_view(views.HotelsAdmin)
    admin.add_view(views.RoomsAdmin)

    return admin
