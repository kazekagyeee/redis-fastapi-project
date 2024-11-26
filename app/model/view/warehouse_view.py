from pydantic import BaseModel

class WarehouseView(BaseModel):
    id: int
    name: str
    address: str
    seller_id: int
