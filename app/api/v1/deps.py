"""
接口层公共依赖：把请求头里的 JWT 换成当前登录用户。
接口这样用：current_user: User = Depends(get_current_user)。
不负责签发 token（那是 app/core/security.py 的事）。
"""

import jwt
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BizError
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer(auto_error=False) #创建了一个 Bearer Token 认证依赖，但不自动拦截错误请求

async def get_current_user(token:  HTTPAuthorizationCredentials = Depends(security),db: AsyncSession = Depends(get_db)):
    if token is None:
        raise BizError("token为空",2003)
    try:
        payload = decode_access_token(token.credentials)  # 过期/伪造会抛异常
    except jwt.InvalidTokenError:
        raise BizError("token错误",2002)
    user_id = payload.get("sub")
    if not user_id:
        raise BizError("token无效",2004)
    user = (
            await db.execute(
            select(User).where(User.id == user_id)
        )).scalar_one_or_none()
    if not user or user.status != 1:
        raise BizError("用户不存在",2005)
    return user
