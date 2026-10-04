"""
Redis 客户端与依赖注入。
Redis 不需要每请求一个连接，全局共用一个客户端即可；
接口层用 r: Redis = Depends(get_redis) 取它。
"""

from redis.asyncio import Redis
from app.core.config import settings

redis_client = Redis.from_url(settings.redis_url, decode_responses=True)

async def get_redis():
    yield redis_client
