import json

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.core.response import success
from app.db.session import get_db
from app.models import User
from app.schemas.product import SpuCreateIn, SpuOut, SpuListItemOut
from app.services.product import create_spu,list_spus as list_spus_service

router = APIRouter(prefix="/api/v1", tags=["商品-详情"])
@router.post("/spus", summary="创建商品")
async def create_product(
        data:SpuCreateIn,
        db: AsyncSession = Depends(get_db),
        _: User = Depends(get_current_user)
):
    cat = await create_spu(db, data)
    return success(SpuOut.model_validate(cat).model_dump(mode="json"))

@router.get("/spus", summary="查询商品价格")
async def list_products(db: AsyncSession = Depends(get_db), page: int = 1, page_size: int = 10):
    rows = await list_spus_service(db, page, page_size)
    data=[]
    for spu, min_price in rows:
        item = SpuListItemOut.model_validate(spu)
        item.min_price = min_price
        data.append(item.model_dump(mode="json"))

    return success(data)

