"""
分类域出入参模型。
CategoryCreateIn：parent_id 可不传（None = 一级分类），sort/status 有默认值。
CategoryOut：只声明结构，不加校验规则。
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class CategoryCreateIn(BaseModel):
    name:str = Field(
    ...,
    max_length=32
    )
    parent_id:int|None=None
    sort:int=0
    status:int=1


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)  #手上是数据库对象、要转成出参模型 → Model.model_validate(obj)，要开这个开关
    id:int
    name :str
    parent_id:int|None=None
    sort:int
    status:int
    created_at:datetime
