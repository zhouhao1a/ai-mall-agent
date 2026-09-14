"""验证登录逻辑。注意：脚本没有上层，所以自己造 session。"""
import asyncio

from app.core.exceptions import BizError
from app.db.session import AsyncSessionLocal, engine
from app.services.user import login, register


async def main():
    async with AsyncSessionLocal() as db:
        # 预置测试号（已存在则忽略）
        try:
            user = await register(db, "13700000001", "123456")
            print("注册成功:", user.id, user.phone, user.created_at)
        except BizError as e:
            print("注册失败:", e.message)

        try:
            user = await login(db, "13700000001", "123456")
            print("登录:", user.id)
        except BizError as e:
            print("登录失败:", e.message)

        try:
            user = await login(db, "13700000001", "wrong_password")
            print("用例3 失败：错误密码居然登录成功了！")  # 不该走到这里
        except BizError as e:
            print("用例3 通过:", e.message)  # 走到这里才是对的

        try:
            user = await login(db, "13700000009", "wrong_password")
            print("用例4 失败：不存在的手机号居然登录成功了！")  # 不该走到这里
        except BizError as e:
            print("用例4 通过:", e.message)  # 走到这里才是对的


    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
