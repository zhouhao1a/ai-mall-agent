from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class UserRegisterIn(BaseModel):
    phone: str = Field(
        ...,
        min_length=11,
        max_length=11,
        pattern=r"^1[3-9]\d{9}$",
    )
    password: str = Field(
        ...,
        description="登录密码，6-72 位",
        min_length=6,
        max_length=72
    )


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    phone: str
    nickname: str
    created_at: datetime


class UserLoginIn(BaseModel):
    phone: str = Field(
        ...,
        min_length=11,
        max_length=11,
        pattern=r"^1[3-9]\d{9}$",
    )
    password: str = Field(
        ...,
        description="登录密码，6-72 位",
        min_length=6,
        max_length=72
    )


class TokenOut(BaseModel):
    token: str
