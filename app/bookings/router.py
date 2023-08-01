from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.auth.schemas import User
from app.bookings.dao import BookingDAO
from app.bookings.exceptions import (BookingNotExistsHTTPException,
                                     NoFreeRoomsLeftHTTPException)
from app.bookings.schemas import (BookingAddSchema, BookingDeleteSchema,
                                  BookingSchema)

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("/count")
async def get_bookings_count(user: Annotated[User, Depends(get_current_user)]):
    return await BookingDAO().get_bookings_count(user_id=user.id)


@router.get("", response_model=list[BookingSchema])
async def get_bookings(user: Annotated[User, Depends(get_current_user)]):
    return await BookingDAO.get_bookings(user_id=user.id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_booking(
    booking: BookingAddSchema,
    user: Annotated[User, Depends(get_current_user)],
):
    new_booking = await BookingDAO().insert_record(
        date_from=booking.date_from,
        date_to=booking.date_to,
        room_id=booking.room_id,
        user_id=user.id,
        email=booking.email,
        first_name=booking.first_name,
        second_name=booking.second_name,
        phone=str(booking.phone),
    )

    if not new_booking:
        raise NoFreeRoomsLeftHTTPException
    return new_booking


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
    booking: BookingDeleteSchema,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    result = await BookingDAO().delete_record(
        booking_id=booking.booking_id, user_id=user.id
    )
    if not result:
        raise BookingNotExistsHTTPException
