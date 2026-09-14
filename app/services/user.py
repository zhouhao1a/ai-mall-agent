from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BizError
from app.core.security import hash_password, verify_password
from app.models.user import User


async def register(db: AsyncSession, phone: str, password: str) -> User:
    """注册新用户，返回创建好的 User 对象。"""

    # ① 查手机号是否已注册
    stmt = select(User).where(User.phone == phone)
    result = await db.execute(stmt)
    exists = result.scalar_one_or_none()

    # ② 已注册 → 抛业务异常（注意：不是 return fail(...)）
    if exists:
        raise BizError("该手机号已注册")

    # ③ 在内存里创建对象，密码先哈希
    user = User(phone=phone, hashed_password=hash_password(password))

    # ④ 写进数据库
    db.add(user)  # 只是登记，不碰数据库，所以不用 await
    try:
        await db.commit()  # ← 这一刻才真正 INSERT
    except IntegrityError:
        # 并发兜底：两个请求同时注册同一手机号，唯一索引会拦下第二个
        await db.rollback()  # 事务坏了，必须先回滚
        raise BizError("该手机号已注册")

    # ⑤ 读回数据库生成的 id 和 created_at
    await db.refresh(user)

    return user


async def login(db: AsyncSession, phone: str, password: str) -> User:
    """登录校验，成功返回 User 对象，失败抛 BizError。"""

    # ① 按手机号查用户（跟 register 里的查重是同一句 SQL）
    stmt = select(User).where(User.phone == phone)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    # ② 用户不存在 或 密码不对 —— 两种失败合并成一个判断
    if not user or not verify_password(password, user.hashed_password):
        raise BizError("手机号或密码错误")

    return user
