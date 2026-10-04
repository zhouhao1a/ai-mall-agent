"""
把各模块的模型集中 import 一遍。
只要 import app.models，Base.metadata 就收集到所有表，
建表脚本和 Alembic 才能看到全部模型。
"""

from app.models.category import Category
from app.models.user import User
from app.models.product import Spu,Sku
