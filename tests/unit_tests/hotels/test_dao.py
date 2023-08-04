import pytest

from app.hotels.dao import HotelsDAO
from app.hotels.models import Hotels


@pytest.mark.hotels
async def test_get_hotel_with_rooms():
    hotel = await HotelsDAO().get_hotel_with_rooms(1)
    if hotel is not None:
        assert hotel.get("id") == 1
        assert hotel.get("name") == 'Отель "Райский уголок"'
        assert hotel.get("location") == "Москва"
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
    hotels = await HotelsDAO().get_hotels(city="мОсКвА")
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
    hotels = await HotelsDAO().get_hotels(stars=stars)
    for hotel in hotels:
        hotel_stars = hotel.get("stars")
        assert hotel_stars is not None and hotel_stars == stars


@pytest.mark.hotels
@pytest.mark.parametrize(
    ("min_price", "max_price"),
    [(0, 10001), (1000, 1001), (40_000, 50_000), (10_000, 5000)],
)
async def test_get_hotels_filtered_by_min_and_max_price(min_price, max_price):
    hotels = await HotelsDAO().get_hotels(min_price=min_price, max_price=max_price)

    if min_price > 10_000 and max_price >= 10_000:
        assert len(hotels) == 0
    if min_price > 10_000:
        assert len(hotels) == 0

    for hotel in hotels:
        hotel_min_price = hotel.get("min_price")
        assert hotel_min_price is not None and hotel_min_price in range(
            min_price, max_price
        )
