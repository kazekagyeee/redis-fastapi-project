from faker import Faker
from redis import asyncio as aioredis
from typing import List
from app import mapper
from app.redis_client import redis_url

mapper = mapper.ModelMapper()
# Создаем экземпляр Faker
faker = Faker('ru_RU')

async def run_migrations():
    """Инициализация структуры данных в Redis."""
    redis = await aioredis.from_url(redis_url, decode_responses=True)

    # Проверяем существование ключа
    if not await redis.exists("items"):
        # Инициализируем пустую коллекцию
        await redis.set("items", "[]")

    if not await redis.exists("sellers"):
        await redis.set("sellers", "[]")

    if not await redis.exists("warehouses"):
        await redis.set("warehouses", "[]")

    for i in range(1, 26):
        item_data = {
            "id": i,
            "name": faker.name(),
            "price": faker.rd_number(),
            "in_stock": int(faker.boolean())
        }
        seller_data = {
            "id": i,
            "name": faker.name()
        }
        warehouse_data = {
            "id": i,
            "name": faker.name(),
            "address": faker.address(),
            "seller_id": i
        }
        await redis.hset(f"item:{i}", mapping=item_data)
        await redis.hset(f"seller:{i}", mapping=seller_data)
        await redis.hset(f"warehouse:{i}", mapping=warehouse_data)

    print("Миграции выполнены.")
    await redis.close()

# Для локального запуска
if __name__ == "__main__":
    import asyncio
    asyncio.run(run_migrations())
