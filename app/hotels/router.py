from asyncio import sleep
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.params import Query
from fastapi_cache.decorator import cache

from app.auth.dependencies import get_current_user
from app.auth.schemas import User
from app.hotels.dao import HotelsDAO
from app.hotels.exceptions import (FavoriteHotelAlreadyExistsDBexception,
                                   FavoriteHotelAlreadyExistsHTTPException,
                                   RecordDoesNotExists)
from app.hotels.schemas import (HotelDetailSchema, HotelFavoriteSchema,
                                HotelSchema)

router = APIRouter(prefix="/hotels", tags=["Отели и комнаты"])


@router.get("/cities")
@cache(expire=15)
async def get_locations(
    request: Request, user: Annotated[User, Depends(get_current_user)]
):
    return await HotelsDAO().get_locations()


@router.post(
    "/favorite",
    status_code=status.HTTP_201_CREATED,
    summary="Добавить избранный отель пользователя",
    responses={
        201: {"description": "Запись добавлена"},
        409: {
            "description": "В таблице уже имеется запись с такими hotel_id и user_id"
        },
    },
)
async def add_favorite_hotel(
    hotel: HotelFavoriteSchema,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    """Добавляет запись избранного отеля пользователя

    Args:
        hotel_id (int): Идентификатор отеля

    Raises:
        FavoriteHotelAlreadyExistsHTTPException: Исключение которое вызывается
        в случае  когда пара user_id и hotel_id уже присутствуют в таблице.

    Returns:
        HTTP 201: Запись создана
        HTTP 409: Запись уже была создана в таблице
    """

    try:
        record_id = await HotelsDAO().add_favorite_hotel(
            user_id=user.id,
            hotel_id=hotel.hotel_id,
        )
    except FavoriteHotelAlreadyExistsDBexception:
        raise FavoriteHotelAlreadyExistsHTTPException

    return record_id


@router.delete(
    "/favorite",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить избранный отель пользователя",
    responses={
        204: {"description": "Запись удалена"},
        404: {"description": "В таблице нет записи с такими hotel_id и user_id"},
    },
)
async def delete_favorite_hotel(
    hotel: HotelFavoriteSchema,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    """Удалить запись избранного отеля пользователя

    Args:
        user_id (int): Идентификатор пользователя
        hotel_id (int): Идентификатор отеля

    Raises:
        RecordDoesNotExists: Вызывает исключение, если в таблице нет записей с таким
        hotel_id и user_id
    """
    result = await HotelsDAO().delete_favorite_hotel(
        user_id=user.id,
        hotel_id=hotel.hotel_id,
    )
    if not result:
        raise RecordDoesNotExists


@router.get("/{id}", response_model=HotelDetailSchema)
async def get_hotel(id: int, user: Annotated[User, Depends(get_current_user)]):
    hotels = await HotelsDAO().get_hotel_with_rooms(hotel_id=id)
    if not hotels:
        return "No hotels"
    return hotels


@router.get("/", response_model=list[HotelSchema])
@cache(15)
async def get_hotels(
    date_from: date | None = None,
    date_to: date | None = None,
    city: str | None = None,
    stars: Annotated[int | None, Query(ge=1, le=5)] = None,
    min_price: Annotated[int | None, Query(ge=0, le=10000)] = 0,
    max_price: Annotated[int | None, Query(ge=0, le=10000)] = 10000,
    favorites_only: bool = False,
):
    if max_price is not None and min_price is not None and max_price < min_price:
        raise HTTPException(
            status_code=400, detail="max_price cannot be less than min_price"
        )
    return await HotelsDAO().get_hotels(
        city=city,
        stars=stars,
        min_price=min_price,
        max_price=max_price,
        favorites_only=favorites_only,
        date_from=date_from,
        date_to=date_to,
    )
