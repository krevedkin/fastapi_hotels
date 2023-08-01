from fastapi import status

from app.exceptions import BaseHTTPException


class FavoriteHotelAlreadyExistsHTTPException(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Данный отель уже есть в списке избранных пользователя"


class FavoriteHotelAlreadyExistsDBexception(Exception):
    message = """
    Запись в БД с такими такими значениями уже существует,
    предоставьте уникальную пару hotel_id и user_id
    """

    def __init__(self):
        super().__init__(self.message)


class RecordDoesNotExists(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Записи не существует"
