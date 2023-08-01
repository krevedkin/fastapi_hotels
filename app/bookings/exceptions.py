from fastapi import status

from app.exceptions import BaseHTTPException


class NoFreeRoomsLeftHTTPException(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT

    detail = "Невозможно забронировать. На эти даты нет сводобных номеров"


class BookingNotExistsHTTPException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Такой записи о бронировании не существует"
