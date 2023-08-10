import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from loguru import logger
from redis import asyncio as aioredis

from app.admin.setup_admin import setup_admin
from app.auth.router import router as auth_router
from app.bookings.router import router as bookings_router
from app.hotels.rooms.router import router as hotels_router
from app.images.router import router as images_router
from app.middleware import handle_exceptions

app = FastAPI()

app.include_router(auth_router)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(images_router)


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(
        "redis://localhost", encoding="utf-8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")


setup_admin(app)

app.middleware("exceptions_handler")(handle_exceptions)

if __name__ == "__main__":
    logger.info(f"App running in mode: {os.environ.get('MODE')}")
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
