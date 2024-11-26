from pydantic import BaseModel
from app.model.seller import Seller

class Warehouse(BaseModel):
    id: int
    name: str
    address: str
    seller: Seller
