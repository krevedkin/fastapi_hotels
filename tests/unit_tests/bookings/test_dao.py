from datetime import date

import pytest

from app.bookings.dao import BookingDAO


@pytest.mark.bookings
async def test_get_bookings():
    bookings = await BookingDAO().get_bookings(user_id=1)

    assert all(booking["user_id"] == 1 for booking in bookings)
    booking_fields = (
        "room_id",
        "user_id",
        "date_from",
        "date_to",
        "price",
        "total_cost",
        "total_days",
        "image_url",
        "room_name",
        "description",
        "services",
        "hotel_name",
    )

    for field in booking_fields:
        assert field in bookings[0]


@pytest.mark.bookings
@pytest.mark.parametrize(
    ("date_from", "date_to"),
    [
        (
            date(2023, 5, 10),
            date(2023, 5, 20),
        ),
        (
            date(2023, 5, 11),
            date(2023, 5, 20),
        ),
        (
            date(2023, 5, 11),
            date(2023, 5, 19),
        ),
        (
            date(2023, 5, 10),
            date(2023, 5, 19),
        ),
        (
            date(2023, 5, 15),
            date(2023, 5, 25),
        ),
        (
            date(2023, 5, 10),
            date(2023, 5, 30),
        ),
        (
            date(2023, 5, 9),
            date(2023, 5, 20),
        ),
        (
            date(2023, 5, 9),
            date(2023, 5, 15),
        ),
    ],
)
async def test_insert_record_full_booked_room(date_from, date_to):
    result = await BookingDAO().insert_record(
        date_from=date_from,
        date_to=date_to,
        room_id=14,
        user_id=1,
        email="user@example.com",
        first_name="user",
        second_name="user",
        phone="12345678901",
    )
    assert result is None


@pytest.mark.bookings
async def test_insert_record_until_no_room():
    for i in range(1, 7):
        booking = await BookingDAO().insert_record(
            date_from=date(2024, 5, 10),
            date_to=date(2024, 5, 20),
            room_id=14,
            user_id=1,
            email="user@example.com",
            first_name="user",
            second_name="user",
            phone="12345678901",
        )
        if i <= 5:
            assert booking is not None
        else:
            assert booking is None


@pytest.mark.bookings
async def test_get_bookings_count():
    count = await BookingDAO().get_bookings_count(1)
    assert isinstance(count, int)
    assert count >= 0
