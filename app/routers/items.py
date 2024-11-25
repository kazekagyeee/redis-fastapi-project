from fastapi import APIRouter, HTTPException
from app.dependencies import redis_client
from app.mapper import ModelMapper
from app.model.item import Item
from app.model.view.item_view import ItemView

router = APIRouter()
mapper = ModelMapper()

@router.post("/items/", response_model=Item)
async def create_item(item: Item):
    redis = redis_client.get_client()
    # Сохраняем объект в Redis как хеш
    await redis.hset(f"item:{item.id}", mapping=mapper.map(item).dict())
    return item

@router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    redis = redis_client.get_client()
    # Получаем объект
    item = await redis.hgetall(f"item:{item_id}")
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Данные уже в виде строк благодаря decode_responses=True
    item = ItemView(**item)

    return mapper.map(item)

@router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    redis = redis_client.get_client()
    # Проверяем существование
    existing_item = await redis.hgetall(f"item:{item_id}")
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Обновляем объект
    await redis.hset(f"item:{item_id}", mapping=mapper.map(item).dict())
    return item

@router.delete("/items/{item_id}")
async def delete_item(item_id: int):
    redis = redis_client.get_client()
    # Проверяем существование
    existing_item = await redis.hgetall(f"item:{item_id}")
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Удаляем объект
    await redis.delete(f"item:{item_id}")
    return {"status": "success", "message": f"Item {item_id} deleted"}
