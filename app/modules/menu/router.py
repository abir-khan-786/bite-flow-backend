from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.core.database import db
from app.modules.auth.dependencies import get_current_user
from app.modules.menu.schemas import CategoryCreateSchema, MenuItemCreateSchema
from prisma.models import User

router = APIRouter(prefix="/api/v1/menu", tags=["Menu"])

# Categories
@router.post("/categories")
async def create_category(data: CategoryCreateSchema, user: User = Depends(get_current_user)):
    category = await db.category.create(
        data={
            "name": data.name,
            "restaurantId": user.restaurantId
        }
    )
    return category

@router.get("/categories")
async def get_categories(user: User = Depends(get_current_user)):
    return await db.category.find_many(
        where={"restaurantId": user.restaurantId},
        include={"menuItems": True}
    )

# Menu Items
@router.post("/items")
async def create_menu_item(data: MenuItemCreateSchema, user: User = Depends(get_current_user)):
    item = await db.menuitem.create(
        data={
            "name": data.name,
            "description": data.description,
            "price": data.price,
            "image": data.image,
            "categoryId": data.categoryId,
            "restaurantId": user.restaurantId
        }
    )
    return item

@router.get("/items")
async def get_menu_items(user: User = Depends(get_current_user)):
    return await db.menuitem.find_many(where={"restaurantId": user.restaurantId})