from datetime import datetime

from sqlalchemy import String, Integer, DateTime, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Category(Base):

    __tablename__ = "categories"     # 数据库里的表名
    __table_args__ = (UniqueConstraint("parent_id", "name"),{"comment": "分类表",})

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="主键ID")
    name:Mapped[str] = mapped_column(String(32),comment="分类名")
    parent_id:Mapped[int | None] = mapped_column(Integer,ForeignKey("categories.id"),nullable=True,comment="父分类 id；一级分类为 NULL")
    sort:Mapped[int] = mapped_column(Integer,comment="同级排序，数字小的靠前")
    status:Mapped[int] = mapped_column(Integer,comment="1 正常 / 0 隐藏")
    created_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now(),comment="创建时间")
    updated_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now(),onupdate=func.now(),comment="更新时间")