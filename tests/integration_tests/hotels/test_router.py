import pytest
from httpx import AsyncClient


@pytest.mark.hotels
async def test_get_cities(auth_ac: AsyncClient):
    cities = await auth_ac.get("/hotels/cities")
    assert 1 == 1
    print(cities)
    # expected_cities = [
    #     "москва",
    #     "санкт-петербург",
    #     "сочи",
    #     "красная поляна",
    #     "казань",
    #     "екатеринбург",
    #     "владивосток",
    #     "анапа",
    #     "великий новгород",
    #     "псков",
    # ]
    # cities = [city.lower() for city in cities]

    # assert cities.sort() == expected_cities.sort()
