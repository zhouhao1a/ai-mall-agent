"""
商品域出入参模型（M3.2 用）。
价格用 Python 的 decimal.Decimal，不是 SQLAlchemy 的 DECIMAL
（后者是数据库列类型，只该出现在 app/models/ 里）。
"""
from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SkuCreateIn(BaseModel):
    title:str
    price:Decimal
    stock:int
    image:str|None=None


class SpuCreateIn(BaseModel):
    category_id:int
    name:str
    subtitle:str|None=None
    main_image:str|None=None
    detail:str|None=None
    skus: list[SkuCreateIn] = Field(..., min_length=1)

class SpuOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    category_id:int
    name:str
    subtitle:str|None
    main_image:str|None
    detail:str|None
    status:int
    created_at:datetime



class SkuOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    spu_id:int
    price:Decimal
    stock:int
    title:str
    image:str|None
    status:int
    created_at:datetime


class SpuListItemOut(SpuOut):
    model_config = ConfigDict(from_attributes=True)
    min_price: Decimal|None=None

class SpuUpdateIn(BaseModel):
    category_id: int| None=None
    name: str|None=None
    subtitle: str | None = None
    main_image: str | None = None
    detail: str | None = None


class SkuUpdateIn(BaseModel):
    price: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    stock: int | None = Field(default=None, ge=0)

class SpuStatusIn(BaseModel):
    status: Literal[0, 1]