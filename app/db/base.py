"""
ORM 基类：所有模型继承它，并统一主键/唯一索引/外键的命名规则。
命名规则让数据库里的约束名字可预测（如 uq_categories_parent_id），
看报错就能定位到是哪张表的哪个约束。
"""

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=naming_convention)
