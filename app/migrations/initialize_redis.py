from redis import asyncio as aioredis
from typing import List
from app.dependencies import redis_url

async def run_migrations():
    """Инициализация структуры данных в Redis."""
    redis = await aioredis.from_url(redis_url, decode_responses=True)

    # Проверяем существование ключа
    if not await redis.exists("items"):
        # Инициализируем пустую коллекцию
        await redis.set("items", "[]")  # Или используйте другую структуру

    # Добавляем предопределенные значения
    initial_items = [
        {"id": 1, "name": "Item 1", "price": 10.0},
        {"id": 2, "name": "Item 2", "price": 20.0}
    ]
    for item in initial_items:
        await redis.hset(f"item:{item['id']}", mapping=item)

    print("Миграции выполнены.")
    await redis.close()

# Для локального запуска
if __name__ == "__main__":
    import asyncio
    asyncio.run(run_migrations())
