"""
用户域接口层：注册 / 登录 / 当前用户 / 改资料 / 取验证码。
只做三件事：收参数、调 service、把结果包成统一响应。业务规则在 app/services/user.py。
"""

from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.core.response import success
from app.core.security import create_access_token
from app.db.redis import get_redis
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserOut, UserRegisterIn, UserLoginIn, TokenOut, UserUpdateIn, SmsCodeIn
from app.services.sms import send_code, verify_code
from app.services.user import register as register_service
from app.services.user import login as login_service
from app.services.user import update_profile

router = APIRouter(prefix="/api/v1/users", tags=["用户"])


@router.post("/register", summary="用户注册")
async def register(data: UserRegisterIn, db: AsyncSession = Depends(get_db),r: Redis = Depends(get_redis)):
    #            ↑ 没默认值，放前面     ↑ 有默认值，放后面
    await verify_code(r, data.phone, data.sms_code)
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
    return success(UserOut.model_validate(current_user).model_dump())  ##model_validate将ORM数据库对象转换成pydantic对象


@router.patch("/me", summary="修改当前登录用户信息")
async def update_me(data: UserUpdateIn, current_user: User = Depends(get_current_user),
                    db: AsyncSession = Depends(get_db)):
    users = await update_profile(db, current_user, data)
    return success(UserOut.model_validate(users).model_dump())  ##model_dump是将pydantic对象转化成json格式


@router.post("/sms/code", summary="获取验证码")
async def sms_code(data: SmsCodeIn, r: Redis = Depends(get_redis)):
    await send_code(r, data.phone)
    return success(message="验证码已发送")
