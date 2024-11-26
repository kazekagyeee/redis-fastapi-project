from pydantic import BaseModel
from app.model.item import Item
from app.model.warehouse import Warehouse

class ItemInWarehouse(BaseModel):
    item: Item
    warehouse: Warehouse
    quantity: int
