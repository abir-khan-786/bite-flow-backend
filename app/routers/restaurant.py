from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import re
from app.db import get_db
from app.models.restaurant import Restaurant
from app.models.user import User, UserRole
from app.schemas.restaurant import RestaurantOut
from app.core.security import hash_password, create_access_token
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

class RestaurantOnboard(BaseModel):
    restaurant_name: str
    owner_email: EmailStr
    password: str

class OnboardOut(BaseModel):
    restaurant: RestaurantOut
    access_token: str
    token_type: str = "bearer"

def generate_slug(name: str) -> str:
    slug = name.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    return slug

@router.post("/onboard", response_model=OnboardOut)
async def onboard_restaurant(data: RestaurantOnboard, db: AsyncSession = Depends(get_db)):
    existing_user = await db.execute(select(User).where(User.email == data.owner_email))
    if existing_user.scalar_one_or_none():
        raise HTTPException(400, "Email already used")

    user = User(email=data.owner_email, hashed_password=hash_password(data.password), role=UserRole.restaurant_owner)
    db.add(user)
    await db.flush()

    base_slug = generate_slug(data.restaurant_name)
    slug = base_slug
    count = 1
    while True:
        existing = await db.execute(select(Restaurant).where(Restaurant.slug == slug))
        if not existing.scalar_one_or_none():
            break
        slug = f"{base_slug}-{count}"
        count += 1

    new_rest = Restaurant(name=data.restaurant_name, slug=slug, owner_email=data.owner_email, owner_id=user.id)
    db.add(new_rest)
    await db.commit()
    await db.refresh(new_rest)

    token = create_access_token({"sub": user.email, "role": user.role.value})
    return {"restaurant": new_rest, "access_token": token, "token_type": "bearer"}

@router.get("/", response_model=list[RestaurantOut])
async def list_restaurants(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Restaurant))
    return result.scalars().all()