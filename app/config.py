from typing import Literal

from loguru import logger
from pydantic import BaseSettings, PostgresDsn, RedisDsn


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"] = "DEV"
    DB_SCHEME: str
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: str

    SECRET_KEY: str
    ALGORITHM: str
    REFRESH_TOKEN_COOKIE_NAME: str = "hotels-app-refresh"
    REFRESH_TOKEN_EXP_DAYS: int = 14
    ACCESS_TOKEN_EXP_MINS: int = 10

    TELEGRAM_TOKEN: str

    @property
    def DATABASE_URL(self):
        return PostgresDsn.build(
            scheme=self.DB_SCHEME,
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=f"/{self.DB_NAME}",
        )

    @property
    def REDIS_URL(self):
        return RedisDsn.build(
            scheme="redis", host=self.REDIS_HOST, port=self.REDIS_PORT
        )

    class Config:
        env_file = ".dev.env"


settings = Settings()  # type: ignore
logger.info(f"App running in {settings.MODE} mode")
