from datetime import date

from pydantic import BaseModel, EmailStr, validator


class BookingAddSchema(BaseModel):
    date_from: date
    date_to: date
    room_id: int
    email: EmailStr
    first_name: str
    second_name: str
    phone: int

    @validator("date_to")
    def date_from_must_be_less_than_date_to(cls, date_to, values):
        date_from = values.get("date_from")
        if date_from and date_from >= date_to:
            raise ValueError("date_to не может быть меньше или равен date_from")

        return date_to

    @validator("phone")
    def phone_must_be_eleven_chars(cls, phone):
        if len(str(phone)) != 11:
            raise ValueError("phone должен содержать ровно 11 цифр")


class BookingDeleteSchema(BaseModel):
    booking_id: int


class BookingSchema(BaseModel):
    booking_id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int
    image_url: str
    room_name: str
    description: str
    services: list
    hotel_name: str
