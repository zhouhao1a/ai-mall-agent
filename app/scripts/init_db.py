"""开发期建表脚本：把 models 里定义的表同步到数据库。"""
import asyncio

from sqlalchemy import text
from sqlalchemy.dialects import mysql
from sqlalchemy.schema import CreateTable
import app.models.user
# # ← 必须 import，否则 Base.metadata 里没有这张表
from app.db.base import Base
from app.db.session import engine


async def main():
    # ① 看看登记册里到底有哪些表
    print("metadata 里登记的表:", list(Base.metadata.tables))

    # ② 把 ORM 生成的建表 SQL 打印出来（只是打印，不执行）
    for table in Base.metadata.sorted_tables:
        print(str(CreateTable(table).compile(dialect=mysql.dialect())).strip())
        print()

    # ③ 真正建表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("建表完成")

    # ④ 看看 MySQL 里现在有哪些表
    async with engine.connect() as conn:
        rows = await conn.execute(text("SHOW TABLES"))
        print("数据库里的表:", [r[0] for r in rows])

    # ⑤ 看看建出来的表长什么样（重点看约束的名字）
    async with engine.connect() as conn:
        row = await conn.execute(text("SHOW CREATE TABLE users"))
        print()
        print(row.one()[1])


if __name__ == "__main__":
    asyncio.run(main())
