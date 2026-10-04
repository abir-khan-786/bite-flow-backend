from pydantic import BaseModel
from typing import Optional

class CategoryCreateSchema(BaseModel):
    name: str

class MenuItemCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image: Optional[str] = None
    categoryId: str