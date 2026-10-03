from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, func, Integer, ForeignKey, String, Text, NUMERIC
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Spu(Base):
    __tablename__ = "spus"
    __table_args__ = {"comment": "商品spu表",}


    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="主键ID")
    category_id:Mapped[int] = mapped_column(Integer,ForeignKey("categories.id"),comment="外键 → categories.id，所属分类")
    name:Mapped[str]=mapped_column(String(128),comment="商品名")
    subtitle:Mapped[str|None]=mapped_column(String(255),comment="副标题，卖点")
    main_image:Mapped[str|None]=mapped_column(String(255),comment="主图 URL")
    detail:Mapped[str|None]=mapped_column(Text,comment="商品详情")
    status:Mapped[int]=mapped_column(Integer,default=1,comment="1 上架 / 0 下架，默认 1")
    created_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now(),comment="创建时间")
    updated_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now(),onupdate=func.now(),comment="更新时间")



class Sku(Base):
    __tablename__ = "skus"
    __table_args__ = {"comment": "商品sku表",}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="主键ID") #autoincrement=True自增
    spu_id:Mapped[int] = mapped_column(Integer,ForeignKey("spus.id"),comment="外键 → spus.id，所属商品")
    title:Mapped[str]=mapped_column(String(128),comment="规格描述")
    price:Mapped[Decimal]=mapped_column(NUMERIC(10,2),comment="价格")
    stock:Mapped[int]=mapped_column(Integer,default=0,comment="库存，默认 0")
    image:Mapped[str|None]=mapped_column(String(255),comment="规格图")
    status:Mapped[int]=mapped_column(Integer,default=1,comment="1 可售 / 0 停售，默认 1")
    created_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now(),comment="创建时间")
    updated_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now(),onupdate=func.now(),comment="更新时间")
