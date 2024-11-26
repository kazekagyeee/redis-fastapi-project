from fastapi import APIRouter, HTTPException
from app.redis_client import redis_client
from app.mapper import ModelMapper
from app.model.seller import Seller
from app.model.view.seller_view import SellerView

router = APIRouter()
mapper = ModelMapper()

@router.post("/sellers/", response_model=Seller)
async def create_seller(seller: Seller):
    redis = redis_client.get_client()
    # Сохраняем объект в Redis как хеш
    await redis.hset(f"seller:{seller.id}", mapping=mapper.map(seller).dict())
    return seller

@router.get("/sellers/{seller_id}", response_model=Seller)
async def get_seller(seller_id: int):
    redis = redis_client.get_client()
    # Получаем объект
    seller = await redis.hgetall(f"seller:{seller_id}")
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    # Данные уже в виде строк благодаря decode_responses=True
    seller = SellerView(**seller)

    return mapper.map(seller)

@router.put("/sellers/{seller_id}", response_model=Seller)
async def update_seller(seller_id: int, seller: Seller):
    redis = redis_client.get_client()
    # Проверяем существование
    existing_seller = await redis.hgetall(f"seller:{seller_id}")
    if not existing_seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    # Обновляем объект
    await redis.hset(f"seller:{seller_id}", mapping=mapper.map(seller).dict())
    return seller

@router.delete("/sellers/{seller_id}")
async def delete_seller(seller_id: int):
    redis = redis_client.get_client()
    # Проверяем существование
    existing_seller = await redis.hgetall(f"seller:{seller_id}")
    if not existing_seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    # Удаляем объект
    await redis.delete(f"seller:{seller_id}")
    return {"status": "success", "message": f"Seller {seller_id} deleted"}
