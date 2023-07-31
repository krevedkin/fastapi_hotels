from typing import Literal
from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"] = "DEV"
    DB_SCHEME: str
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str
    REFRESH_TOKEN_COOKIE_NAME: str = "hotels-app-refresh"
    REFRESH_TOKEN_EXP_DAYS: int = 14
    ACCESS_TOKEN_EXP_MINS: int = 10

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

    class Config:
        env_file = ".dev.env"


# def get_settings() -> Settings:
#     mode = os.environ.get("HOTELS_APP_MODE")
#     # if mode == "DEV":
#     #     return Settings(_env_file=".env")
#     if mode == "TEST":
#         return Settings(_env_file=".env-test")
#     # return Settings(_env_file=".env-test")

#     raise FileNotFoundError("Не найден файл .env с настройками приложения")


settings = Settings()
print(settings.MODE)
