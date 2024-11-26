from pydantic import BaseModel

class SellerView(BaseModel):
    id: int
    name: str
