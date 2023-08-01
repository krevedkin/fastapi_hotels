from datetime import datetime
from pydantic import BaseModel, EmailStr, UUID4, Field


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class RefreshToken(BaseModel):
    refresh_token: UUID4
    expire: datetime


class User(BaseModel):
    id: int
    email: EmailStr


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
