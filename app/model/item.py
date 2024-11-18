from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    id: Optional[int] = None  # ID может быть не обязательным (для создания)
    name: str
    price: float
    in_stock: bool
