from fastapi import status

from app.exceptions import BaseHTTPException


class FileNameIsNoneHTTPException(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "У переданного файла нет имени. Предоставьте файл с именем"
