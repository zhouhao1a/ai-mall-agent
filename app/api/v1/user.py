from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.core.response import success
from app.core.security import create_access_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserOut, UserRegisterIn, UserLoginIn, TokenOut
from app.services.user import register as register_service
from app.services.user import login as login_service

router = APIRouter(prefix="/api/v1/users", tags=["用户"])


@router.post("/register", summary="用户注册")
async def register(data: UserRegisterIn, db: AsyncSession = Depends(get_db)):
    #            ↑ 没默认值，放前面     ↑ 有默认值，放后面

    user = await register_service(db, data.phone, data.password)
    #                          ↑ 手动把 db 传下去

    return success(UserOut.model_validate(user).model_dump())


@router.post("/login", summary="用户登录")
async def login(data: UserLoginIn, db: AsyncSession = Depends(get_db)):
    #            ↑ 没默认值，放前面     ↑ 有默认值，放后面

    user = await login_service(db, data.phone, data.password)

    token = create_access_token(user.id)
    return success(TokenOut(token=token).model_dump())


@router.get("/me", summary="获取当前登录用户信息")
async def me(current_user: User = Depends(get_current_user)):
    return success(UserOut.model_validate(current_user).model_dump())
