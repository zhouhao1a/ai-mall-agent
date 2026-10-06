from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BizError
from app.models import Spu, Category, Sku
from app.schemas.product import SpuCreateIn


async def create_spu(db:AsyncSession, data:SpuCreateIn) -> Spu:
    cate = await db.get(Category, data.category_id)
    if cate is None:
        raise BizError("分类不存在",code=3003)

    spu = Spu(category_id=data.category_id, name=data.name,subtitle=data.subtitle,main_image=data.main_image,detail=data.detail)
    db.add(spu)
    try:
        await db.flush()
        for sku in data.skus:
            db.add(Sku(spu_id=spu.id,title=sku.title,price=sku.price,stock=sku.stock,image=sku.image))
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise BizError("商品创建失败，请重试",code=3004)
    await db.refresh(spu)
    return spu
