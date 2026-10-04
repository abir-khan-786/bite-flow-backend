from pydantic import BaseModel
import uuid

class RestaurantCreate(BaseModel):
    name: str
    owner_email: str

class RestaurantOut(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    owner_email: str
    owner_id: uuid.UUID | None
    is_active: bool
    class Config:
        from_attributes = True