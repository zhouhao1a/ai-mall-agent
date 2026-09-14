"""验证注册逻辑。注意：脚本没有上层，所以自己造 session。"""
import asyncio

from app.core.exceptions import BizError
from app.db.session import AsyncSessionLocal, engine
from app.services.user import register


async def main():
    async with AsyncSessionLocal() as db:
        # 第一次：正常注册
        try:
            user = await register(db, "13900000001", "123456")
            print("注册成功:", user.id, user.phone, user.created_at)
        except BizError as e:
            print("注册失败:", e.message)

        # 第二次：同一个手机号再注册
        try:
            user = await register(db, "13900000001", "123456")
            print("注册成功:", user.id)
        except BizError as e:
            print("第二次注册:", e.message)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
