from datetime import datetime, timezone, timedelta
import bcrypt
import jwt

from app.core.config import settings


def hash_password(plain: str) -> str:
    """把明文密码变成哈希串，用于存数据库。"""
    pwd_bytes = plain.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_bytes.decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    # 验证明文密码和数据库里的哈希串是否匹配。
    pwd_bytes = plain.encode("utf-8")
    hashed_bytes = hashed.encode("utf-8")
    return bcrypt.checkpw(pwd_bytes,hashed_bytes)

def create_access_token(user_id: int) -> str:
# 给用户签发一张通行证（token）。
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def decode_access_token(token: str) -> dict | None:
  # 解开通行证。有效返回 payload，无效（过期/被篡改）返回 None。
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None