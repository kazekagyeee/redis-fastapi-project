from fastapi import APIRouter, HTTPException
from app.model.view.warehouse_view import WarehouseView
from app.model.warehouse import Warehouse
from app.redis_client import redis_client
from app.mapper import ModelMapper
from app.model.seller import Seller
from app.model.view.seller_view import SellerView

router = APIRouter()
mapper = ModelMapper()

@router.post("/warehouses/", response_model=Warehouse)
async def create_warehouse(warehouse: Warehouse):
    redis = redis_client.get_client()
    # Сохраняем объект в Redis как хеш
    await redis.hset(f"warehouse:{warehouse.id}", mapping=mapper.map(warehouse).dict())
    return warehouse

@router.get("/warehouses/{warehouse_id}", response_model=Warehouse)
async def get_warehouse(warehouse_id: int):
    redis = redis_client.get_client()
    # Получаем объект
    warehouse = await redis.hgetall(f"warehouse:{warehouse_id}")
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")

    # Данные уже в виде строк благодаря decode_responses=True
    warehouse = WarehouseView(**warehouse)

    return mapper.map(warehouse)

@router.put("/warehouses/{warehouse_id}", response_model=Warehouse)
async def update_warehouse(warehouse_id: int, warehouse: Warehouse):
    redis = redis_client.get_client()
    # Проверяем существование
    existing_warehouse = await redis.hgetall(f"seller:{warehouse_id}")
    if not existing_warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")

    # Обновляем объект
    await redis.hset(f"warehouse:{warehouse_id}", mapping=mapper.map(warehouse).dict())
    return warehouse

@router.delete("/warehouses/{warehouse_id}")
async def delete_warehouse(warehouse_id: int):
    redis = redis_client.get_client()
    # Проверяем существование
    existing_warehouse = await redis.hgetall(f"warehouse:{warehouse_id}")
    if not existing_warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")

    # Удаляем объект
    await redis.delete(f"warehouse:{warehouse_id}")
    return {"status": "success", "message": f"Warehouse {warehouse_id} deleted"}
