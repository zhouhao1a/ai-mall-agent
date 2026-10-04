"""
分类域服务层：创建分类、查询分类列表。
创建流程：验父（parent_id 非空时）→ 同级查重 → 造对象 → 入库（含并发兜底）。
错误码：3001 同级重名 / 3002 父分类不存在。
"""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BizError
from app.models import Category
from app.schemas.category import CategoryCreateIn

async def create_category(
        db: AsyncSession,
        data:CategoryCreateIn
)-> Category:
    if data.parent_id is not None:
        cate=await db.get(Category, data.parent_id)
        if cate is None:
            raise BizError("父分类不存在",code=3002)
    stmt = select(Category).where(Category.parent_id ==data.parent_id,Category.name==data.name)
    result = await db.execute(stmt)
    exists = result.scalar_one_or_none()  # 捞不到 → None；捞到 → User 对象
    if exists:
        raise BizError("同级下已存在同名分类", code=3001)
    category = Category(parent_id=data.parent_id,name=data.name,sort=data.sort,status=data.status)
    db.add(category)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()  # 事务坏了，必须先回滚
        raise BizError("同名分类被并发插入",code=3001)
    await db.refresh(category)

    return category

async  def list_categories(db: AsyncSession):
    stmt=select(Category).order_by(Category.sort,Category.id)
    result=await db.execute(stmt)
    return result.scalars().all()
