from pydantic import BaseModel, EmailStr
from typing import Optional
from prisma.enums import UserRole

class RestaurantRegisterSchema(BaseModel):
    restaurant_name: str
    slug: str
    owner_name: str
    email: EmailStr
    phone: str
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict