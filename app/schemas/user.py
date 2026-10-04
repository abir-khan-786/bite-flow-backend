from pydantic import BaseModel, EmailStr
import uuid
from app.models.user import UserRole

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: uuid.UUID
    email: str
    role: UserRole
    is_active: bool
    class Config:
        from_attributes = True

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut