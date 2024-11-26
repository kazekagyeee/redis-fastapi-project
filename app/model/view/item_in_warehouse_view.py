from pydantic import BaseModel

class ItemInWarehouseView(BaseModel):
    item_id: int
    warehouse_id: int
    quantity: int
