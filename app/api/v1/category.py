"""
分类接口层：创建分类（需登录）、查询分类列表（公开）。
业务规则在 app/services/category.py。
"""

from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.core.response import success
from app.db.session import get_db
from app.models import User
from app.schemas.category import CategoryCreateIn, CategoryOut
from app.services.category import create_category as create_category_service, list_categories as list_categories_service

router = APIRouter(prefix="/api/v1", tags=["商品-分类"])

@router.post("/categories", summary="创建分类")
async def create_category(
        data: CategoryCreateIn,
        db: AsyncSession = Depends(get_db),
        _: User = Depends(get_current_user),
):
    cat = await create_category_service(db, data)
    return success(CategoryOut.model_validate(cat).model_dump())

@router.get("/categories", summary="查询分类")
async def list_categories(
        db: AsyncSession = Depends(get_db),
):
    cats=await list_categories_service(db)
    return success([CategoryOut.model_validate(c).model_dump() for c in cats])
