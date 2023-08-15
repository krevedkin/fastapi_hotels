from datetime import date

import pytest

from app.hotels.dao import HotelsDAO
from app.hotels.exceptions import FavoriteHotelAlreadyExistsDBexception


@pytest.mark.hotels
async def test_get_hotel_with_rooms():
    hotel = await HotelsDAO().get_hotel_with_rooms(1)
    if hotel is not None:
        assert hotel.get("id") == 1
        assert hotel.get("name") == 'Отель "Райский уголок"'
        assert hotel.get("services") == ["Спа", "Бассейн", "Ресторан"]
        assert hotel.get("rooms_quantity") == 50
        assert (
            hotel.get("image_url")
            == "http://localhost:8000/static/images/hotels/1.webp"
        )
        assert hotel.get("stars") == 1
        assert hotel.get("description") == "Роскошный отель с первоклассными удобствами"
        assert hotel.get("city") == "Москва"
        assert hotel.get("address") == "ул. Тверская, д. 123"
        rooms = hotel.get("rooms")
        assert rooms is not None
        assert len(rooms) != 0
        assert await HotelsDAO().get_hotel_with_rooms(1000) is None


@pytest.mark.hotels
async def test_get_hotels_filtered_by_city():
    hotels = await HotelsDAO().get_hotels(user_id=1, city="мОсКвА")
    assert len(hotels) != 0
    for hotel in hotels:
        hotel_city = hotel.get("city")
        assert hotel_city is not None
        assert hotel_city == "Москва"


@pytest.mark.hotels
@pytest.mark.parametrize(
    ("stars"),
    [1, 2, 3, 4, 5],
)
async def test_get_hotels_filtered_by_stars(stars):
    hotels = await HotelsDAO().get_hotels(user_id=1, stars=stars)
    for hotel in hotels:
        hotel_stars = hotel.get("stars")
        assert hotel_stars is not None and hotel_stars == stars


@pytest.mark.hotels
@pytest.mark.parametrize(
    ("min_price", "max_price"),
    [(0, 10001), (1000, 1001), (40_000, 50_000), (10_000, 5000)],
)
async def test_get_hotels_filtered_by_min_and_max_price(min_price, max_price):
    hotels = await HotelsDAO().get_hotels(
        user_id=1, min_price=min_price, max_price=max_price
    )

    if min_price > 10_000 and max_price >= 10_000:
        assert len(hotels) == 0
    if min_price > 10_000:
        assert len(hotels) == 0

    for hotel in hotels:
        hotel_min_price = hotel.get("min_price")
        assert hotel_min_price is not None and hotel_min_price in range(
            min_price, max_price
        )


@pytest.mark.hotels
@pytest.mark.parametrize(("is_favorite"), [(True), [False]])
async def test_get_hotels_filtered_by_favorites_only(is_favorite):
    hotels = await HotelsDAO().get_hotels(user_id=1, favorites_only=is_favorite)

    if is_favorite:
        assert all([hotel["is_favorite"] for hotel in hotels])
    else:
        assert any([hotel["is_favorite"] for hotel in hotels])


@pytest.mark.hotels
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
async def test_get_hotels_filtered_by_dates_not_include_full_booked_hotel(
    date_from, date_to
):
    hotels = await HotelsDAO().get_hotels(
        user_id=1,
        date_from=date_from,
        date_to=date_to,
    )

    hotels_names = [hotel["name"] for hotel in hotels]
    assert len(hotels_names) == len(set(hotels_names))
    for hotel in hotels:
        assert hotel["name"] != "Отель с забронированными номерами"


@pytest.mark.hotels
@pytest.mark.parametrize(
    ("date_from", "date_to"),
    [
        (
            date(2023, 5, 1),
            date(2023, 5, 9),
        ),
        (
            date(2023, 5, 21),
            date(2023, 5, 30),
        ),
    ],
)
async def test_get_hotels_filtered_by_dates_includes_full_booked_hotel(
    date_from, date_to
):
    hotels = await HotelsDAO().get_hotels(
        user_id=1,
        date_from=date_from,
        date_to=date_to,
    )
    hotels_names = [hotel["name"] for hotel in hotels]
    assert len(hotels_names) == len(set(hotels_names))
    assert any(
        [hotel["name"] == "Отель с забронированными номерами" for hotel in hotels]
    )


@pytest.mark.hotels
async def test_get_cities():
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
    cities = await HotelsDAO().get_locations()
    cities = [city.lower() for city in cities]

    assert cities.sort() == expected_cities.sort()


@pytest.mark.hotels
@pytest.mark.parametrize(
    (
        "hotel_id",
        "user_id",
    ),
    [
        (2, 1),
        (2, 2),
    ],
)
async def test_add_favorite_hotel(
    user_id,
    hotel_id,
):
    favorite_hotel_id = await HotelsDAO().add_favorite_hotel(
        hotel_id=hotel_id, user_id=user_id
    )
    if favorite_hotel_id is not None:
        assert "id" in favorite_hotel_id
        assert isinstance(favorite_hotel_id["id"], int)

    with pytest.raises(FavoriteHotelAlreadyExistsDBexception):
        await HotelsDAO().add_favorite_hotel(hotel_id=1, user_id=1)


@pytest.mark.hotels
async def test_delete_favorite_hotel():
    assert await HotelsDAO().delete_favorite_hotel(user_id=1, hotel_id=1) is True
    assert await HotelsDAO().delete_favorite_hotel(user_id=1, hotel_id=10) is False
