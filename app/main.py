import os
from loguru import logger
import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.bookings.router import router as bookings_router
from app.hotels.rooms.router import router as hotels_router

from app.auth.router import router as auth_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(bookings_router)
app.include_router(hotels_router)

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
if __name__ == "__main__":
    logger.info(f"App running in mode: {os.environ.get('MODE')}")
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
