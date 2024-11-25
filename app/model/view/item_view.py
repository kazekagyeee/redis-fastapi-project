from pydantic import BaseModel

class ItemView(BaseModel):
    id: int
    name: str
    price: float
    in_stock: int
