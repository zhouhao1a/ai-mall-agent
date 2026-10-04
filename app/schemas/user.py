"""
用户域出入参模型（pydantic）。
分界线：入参（XxxIn）带校验规则，出参（UserOut）只声明结构不校验。
UserOut 开了 from_attributes=True，才能直接吃 ORM 对象。
"""

from datetime import datetime
from typing import Optional

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
    sms_code:str=Field(
        ...,
        min_length=6,
        max_length=6,
        pattern=r"^\d{6}$"
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


class UserUpdateIn(BaseModel):
    nickname:Optional[str]=Field(
        None,
        max_length=32
    )

class SmsCodeIn(BaseModel):
    phone: str = Field(
        ...,
        min_length=11,
        max_length=11,
        pattern=r"^1[3-9]\d{9}$",
    )
