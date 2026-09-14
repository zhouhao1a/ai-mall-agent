# 创建异步引擎：相当于打开一条通往MySQL的通道
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.core.config import settings
from app.db.base import Base

engine = create_async_engine(settings.database_url, echo=settings.app_env == "dev",pool_pre_ping=True,)

# 创建会话工厂：以后每次读写数据库，就从这里拿一个会话.一个事务
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)



#就是个依赖，定义函数时让带上，类似于鉴权的依赖
async def get_db():
  async with AsyncSessionLocal() as session:
      try:
          yield session
      except Exception:
          await session.rollback()
          raise
      finally:
          await session.close()