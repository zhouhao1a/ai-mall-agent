import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer(auto_error=False)

async def get_current_user(token:  HTTPAuthorizationCredentials = Depends(security),db: AsyncSession = Depends(get_db)):
    if token is None:
        raise HTTPException(status_code=401, detail="token为空")
    try:
        payload = decode_access_token(token.credentials)  # 过期/伪造会抛异常
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="token错误")
    user_id = payload["sub"]
    user = (
            await db.execute(
            select(User).where(User.id == user_id)
        )).scalar_one_or_none()
    if not user or user.status != 1:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user