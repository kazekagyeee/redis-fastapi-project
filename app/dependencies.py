from typing import Optional
from redis import asyncio as aioredis

redis_url = "redis://localhost:6379"

class RedisClient:
    def __init__(self):
        self.redis_url = redis_url
        self.redis: Optional[aioredis.Redis] = None  # Типизация для IDE

    async def connect(self):
        """Устанавливает соединение с Redis."""
        self.redis = await aioredis.from_url(self.redis_url, decode_responses=True)

    async def disconnect(self):
        """Закрывает соединение с Redis, если оно есть."""
        if self.redis:
            await self.redis.close()
            self.redis = None

    def get_client(self) -> aioredis.Redis:
        """Возвращает активное соединение, если оно установлено."""
        if not self.redis:
            raise RuntimeError("Redis connection is not established. Call 'connect' first.")
        return self.redis

redis_client = RedisClient()
