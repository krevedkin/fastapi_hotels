import pytest
from httpx import AsyncClient


@pytest.mark.bookings
async def test_get_bookings_count(auth_ac: AsyncClient):
    response = await auth_ac.get("/bookings/count")
    assert response.status_code == 200
    assert isinstance(response.json(), int)
    assert response.json() >= 0


@pytest.mark.bookings
async def test_get_bookings(auth_ac: AsyncClient):
    response = await auth_ac.get("/bookings")
    assert response.status_code == 200

    bookings = response.json()
    booking_fileds = (
        "room_id",
        "user_id",
        "date_from",
        "date_to",
        "price",
    )

    for field in booking_fileds:
        assert field in bookings[0]

    assert all([booking["user_id"] == 1 for booking in bookings])


@pytest.mark.bookings
async def test_add_booking(auth_ac: AsyncClient):
    response = await auth_ac.post(
        "/bookings",
        json={
            "date_from": "2024-06-10",
            "date_to": "2024-06-20",
            "room_id": 14,
            "email": "user@example.com",
            "first_name": "user",
            "second_name": "user",
            "phone": "12345678901",
        },
    )
    assert response.status_code == 201


@pytest.mark.bookings
@pytest.mark.parametrize(
    ("date_from", "date_to", "phone"),
    [
        (
            "2024-06-10",
            "2024-05-20",
            "12345678901",
        ),
        (
            "2024-06-10",
            "2024-06-20",
            "1234567890",
        ),
    ],
)
async def test_add_booking_dates_and_phone_validation(
    date_from,
    date_to,
    phone,
    auth_ac: AsyncClient,
):
    response = await auth_ac.post(
        "/bookings",
        json={
            "date_from": date_from,
            "date_to": date_to,
            "room_id": 14,
            "email": "user@example.com",
            "first_name": "user",
            "second_name": "user",
            "phone": phone,
        },
    )
    assert response.status_code == 422


@pytest.mark.bookings
async def test_add_booking_with_no_free_rooms(auth_ac: AsyncClient):
    response = await auth_ac.post(
        "/bookings",
        json={
            "date_from": "2023-05-10",
            "date_to": "2024-05-20",
            "room_id": 14,
            "email": "user@example.com",
            "first_name": "user",
            "second_name": "user",
            "phone": "12345678901",
        },
    )

    assert response.status_code == 409


@pytest.mark.bookings
@pytest.mark.parametrize(
    ("booking_id", "status_code"),
    [
        (100, 404),
    ],
)
async def test_delete_bookings(booking_id, status_code, auth_ac: AsyncClient):
    response = await auth_ac.request(
        method="delete",
        url="/booking",
        json={
            "booking_id": booking_id,
        },
    )
    assert response.status_code == status_code
