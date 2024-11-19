from fastapi import FastAPI
from app.routers import items
from app.dependencies import redis_client
import app.migrations.initialize_redis as initialize_redis

app = FastAPI()

# Подключаем маршруты
app.include_router(items.router)

# События старта и остановки приложения
@app.on_event("startup")
async def startup_event():
    await redis_client.connect()
    await initialize_redis.run_migrations()

@app.on_event("shutdown")
async def shutdown_event():
    await redis_client.disconnect()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI with Redis!"}
