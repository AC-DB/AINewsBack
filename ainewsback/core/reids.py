import redis.asyncio as redis
from typing import Optional
from ainewsback.core.config import settings

class AsyncRedisClient:
    """Redis 客户端单例"""
    _instance: Optional[redis.Redis] = None

    @classmethod
    async def get_client(cls) -> redis.Redis:
        """获取 Redis 客户端实例"""
        if cls._instance is None:
            cls._instance = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
                decode_responses=settings.REDIS_DECODE_RESPONSES,
                socket_connect_timeout=5,
                socket_keepalive=True,
                health_check_interval=30
            )
        return cls._instance

    @classmethod
    async def close(cls):
        """关闭 Redis 连接"""
        if cls._instance:
            await cls._instance.close()
            cls._instance = None


async def get_redis() -> redis.Redis:
    """依赖注入函数"""
    return await AsyncRedisClient.get_client()