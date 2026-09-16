from datetime import datetime
from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class User(Base):
    """用户表：电商系统的账号主体。购物车、订单、地址等业务数据最终都挂在它下面。"""

    __tablename__ = "users"     # 数据库里的表名
    __table_args__ = {"comment": "用户表"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="主键ID")
    phone: Mapped[str] = mapped_column(String(11), unique=True, comment="手机号，登录账号，全局唯一")
    hashed_password: Mapped[str] = mapped_column(String(128), comment="bcrypt 哈希后的密码，禁止存明文")
    nickname: Mapped[str] = mapped_column(String(32), default="", comment="昵称，注册后可在个人资料里修改")
    status: Mapped[int] = mapped_column(Integer, default=1, comment="账号状态：1=正常，0=禁用(封号)")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), comment="最后更新时间")
