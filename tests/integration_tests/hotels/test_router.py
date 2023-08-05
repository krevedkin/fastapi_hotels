from datetime import date

import pytest
from httpx import AsyncClient


@pytest.mark.hotels
async def test_get_cities(auth_ac: AsyncClient):
    response = await auth_ac.get("/hotels/cities")
    cities = response.json()
    assert response.status_code == 200
    expected_cities = [
        "москва",
        "санкт-петербург",
        "сочи",
        "красная поляна",
        "казань",
        "екатеринбург",
        "владивосток",
        "анапа",
        "великий новгород",
        "псков",
    ]
    cities = [city.lower() for city in cities]

    assert cities.sort() == expected_cities.sort()


@pytest.mark.hotels
@pytest.mark.parametrize(("hotel_id", "status_code"), [(1, 409), (5, 201)])
async def test_add_favorite_hotel(hotel_id, status_code, auth_ac: AsyncClient):
    response = await auth_ac.post(
        "/hotels/favorite",
        json={"hotel_id": hotel_id},
    )
    assert response.status_code == status_code

    if response.status_code == 409:
        assert (
            response.json()["detail"]
            == "Данный отель уже есть в списке избранных пользователя"
        )


@pytest.mark.hotels
@pytest.mark.parametrize(("hotel_id", "status_code"), [(5, 204), (5, 404)])
async def test_delete_favorite_hotel(hotel_id, status_code, auth_ac: AsyncClient):
    response = await auth_ac.request(
        "delete",
        "/hotels/favorite",
        json={"hotel_id": hotel_id},
    )

    assert response.status_code == status_code

    if response.status_code == 404:
        assert response.json()["detail"] == "Записи не существует"


@pytest.mark.hotels
@pytest.mark.parametrize(("hotel_id", "status_code"), [(1, 200), (500, 404)])
async def test_get_hotel(hotel_id, status_code, auth_ac: AsyncClient):
    response = await auth_ac.get(f"/hotels/{hotel_id}")
    assert response.status_code == status_code


@pytest.mark.hotels
@pytest.mark.parametrize(
    ("date_from", "date_to", "has_full_booked_hotel"),
    [
        (
            date(2023, 5, 10),
            date(2023, 5, 20),
            False,
        ),
        (
            date(2023, 5, 5),
            date(2023, 5, 15),
            False,
        ),
        (
            date(2023, 5, 5),
            date(2023, 5, 25),
            False,
        ),
        (
            date(2023, 5, 5),
            date(2023, 5, 9),
            True,
        ),
        (
            date(2023, 5, 21),
            date(2023, 5, 30),
            True,
        ),
    ],
)
async def test_get_hotels_filtered_by_dates(
    date_from, date_to, has_full_booked_hotel, auth_ac: AsyncClient
):
    response = await auth_ac.get(
        "/hotels/", params={"date_from": date_from, "date_to": date_to}
    )
    assert response.status_code == 200

    hotels = response.json()

    if has_full_booked_hotel:
        assert any(
            [hotel["name"] == "Отель с забронированными номерами" for hotel in hotels]
        )
    else:
        assert all(
            [hotel["name"] != "Отель с забронированными номерами" for hotel in hotels]
        )


@pytest.mark.hotels
@pytest.mark.parametrize(
    ("city"),
    [
        "москва",
        "не существует",
    ],
)
async def test_get_hotels_filtered_by_city(city, auth_ac: AsyncClient):
    response = await auth_ac.get("/hotels/", params={"city": city})

    assert response.status_code == 200
    if city == "москва":
        assert all([hotel["city"].lower() == "москва" for hotel in response.json()])

    if city == "не существует":
        assert response.json() == []


@pytest.mark.hotels
@pytest.mark.parametrize(
    ("stars", "status_code"),
    [(5, 200), (0, 422), (6, 422), (-1, 422)],
)
async def test_get_hotels_filtered_by_stars(stars, status_code, auth_ac: AsyncClient):
    response = await auth_ac.get("/hotels/", params={"stars": stars})

    assert response.status_code == status_code
    if stars in range(1, 6):
        assert all([hotel["stars"] == stars for hotel in response.json()])


@pytest.mark.hotels
@pytest.mark.parametrize(
    ("min_price", "max_price", "status_code"),
    [(0, 10_000, 200), (5000, 6000, 200), (-2000, 5000, 422), (1000, 10_001, 422)],
)
async def test_get_hotels_filtered_by_price(
    min_price, max_price, status_code, auth_ac: AsyncClient
):
    response = await auth_ac.get(
        "/hotels/",
        params={
            "max_price": max_price,
            "min_price": min_price,
        },
    )

    assert response.status_code == status_code


@pytest.mark.hotels
async def test_get_hotels_filtered_by_favorites_only(auth_ac: AsyncClient):
    response = await auth_ac.get(
        "/hotels/",
        params={
            "favorites_only": True,
        },
    )

    assert response.status_code == 200
    assert all([hotel["is_favorite"] for hotel in response.json()])
