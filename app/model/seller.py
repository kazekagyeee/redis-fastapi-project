from pydantic import BaseModel

class Seller(BaseModel):
    id: int
    name: str
