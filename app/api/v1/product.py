from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.core.response import success
from app.db.session import get_db
from app.models import User
from app.schemas.product import SpuCreateIn, SpuOut
from app.services.product import create_spu

router = APIRouter(prefix="/api/v1", tags=["商品-详情"])
@router.post("/spus", summary="创建商品")
async def create_product(
        data:SpuCreateIn,
        db: AsyncSession = Depends(get_db),
        _: User = Depends(get_current_user)
):
    cat = await create_spu(db, data)
    return success(SpuOut.model_validate(cat).model_dump())


