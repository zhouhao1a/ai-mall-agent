"""
短信验证码（开发期是假短信：验证码打印到控制台，不接服务商）。
Redis 两类 key，都用 TTL 到期自动清理：
  sms:limit:{phone}  发送频控 EX 60，60 秒内只能发一次
  sms:code:{phone}   验证码本体 EX 300，校验通过后删除（一次性）
"""

import secrets
from redis.asyncio import Redis

from app.core.exceptions import BizError


async def send_code(r: Redis, phone) -> None:
    """生成 6 位验证码存进 Redis，300 秒过期"""
    limit_key = f"sms:limit:{phone}"
    limit = await r.set(limit_key, 1, ex=60, nx=True)
    if not limit:
        raise BizError("验证码发送过于频繁，请稍后再试")
    key = f"sms:code:{phone}"  # 获取k值
    code = str(secrets.randbelow(900000) + 100000)  # 获取验证码
    await r.set(key, code, ex=300)  # 获取k值 → key值；#取得时候靠键取值 → 靠键取值
    print(f"模拟短信服务商:{code}")


async def verify_code(r: Redis, phone, code):
    """校验验证码，失败抛 BizError；成功则立刻删除（一次性）。"""
    key = f"sms:code:{phone}"  # 获取k值
    code_value = await r.get(key)
    if not code_value:
        raise BizError("已过期/没发过")
    if code_value != code:
        raise BizError("验证码错误")
    await r.delete(key)
