from decimal import Decimal

from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BizError
from app.models import Spu, Category, Sku
from app.schemas.product import SpuCreateIn, SpuUpdateIn


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


async def list_spus(db:AsyncSession, page: int, page_size: int ) -> list[tuple[Spu, Decimal | None]]:

    stmt=(
        select(Spu,func.min(Sku.price))   # 我要：SPU 整行 + 一个"最低价"列
        .outerjoin(Sku,Sku.spu_id==Spu.id)    #把 skus 接上来（outerjoin = LEFT JOIN）
        .group_by(Spu.id)                      # 按商品分组，才能对每组求 min
        .order_by(Spu.id.desc())               # 排序
        .limit(page_size).offset((page-1) * page_size) # 分页
    )
    rows = (await db.execute(stmt)).all()
    return [(spu, min_price) for spu, min_price in rows]



async def update_spu(db:AsyncSession, spu_id:int, data:SpuUpdateIn)->Spu:
    spu = await db.get(Spu, spu_id)
    if spu is None:
        raise BizError("商品不存在",code=3005)
    payload = data.model_dump(exclude_unset=True)
    for k, v in payload.items():
        setattr(spu, k, v)
    await db.commit()
    await db.refresh(spu)
    return spu
