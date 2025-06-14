from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from typing import Optional, Any
import json

async def setup_cache():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="construction-cache")

class CacheManager:
    @staticmethod
    async def get(key: str) -> Optional[Any]:
        try:
            return await FastAPICache.get(key)
        except Exception:
            return None

    @staticmethod
    async def set(key: str, value: Any, expire: int = 300):
        try:
            await FastAPICache.set(key, value, expire=expire)
        except Exception:
            pass

    @staticmethod
    async def delete(key: str):
        try:
            await FastAPICache.delete(key)
        except Exception:
            pass

    @staticmethod
    async def clear():
        try:
            await FastAPICache.clear()
        except Exception:
            pass

# 캐시 데코레이터 예시
def cache_response(expire: int = 300):
    def decorator(func):
        @cache(expire=expire)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper
    return decorator 