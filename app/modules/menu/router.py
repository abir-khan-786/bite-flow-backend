from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.core.database import db
from app.modules.auth.dependencies import get_current_user
from app.modules.menu.schemas import CategoryCreateSchema, MenuItemCreateSchema
from prisma.models import User
from prisma.types import CategoryCreateInput, MenuItemCreateInput

router = APIRouter(prefix="/api/v1/menu", tags=["Menu"])

# ==========================================
# CATEGORIES
# ==========================================

@router.post("/categories")
async def create_category(data: CategoryCreateSchema, user: User = Depends(get_current_user)):
    if not user.restaurantId:
        raise HTTPException(
            status_code=400, 
            detail="User is not assigned to any restaurant"
        )

    category_data: CategoryCreateInput = {
        "name": data.name,
        "restaurant": {
            "connect": {"id": user.restaurantId}
        }
    }

    category = await db.category.create(data=category_data)
    return category


@router.get("/categories")
async def get_categories(user: User = Depends(get_current_user)):
    if not user.restaurantId:
        raise HTTPException(
            status_code=400, 
            detail="User is not assigned to any restaurant"
        )

    return await db.category.find_many(
        where={"restaurantId": user.restaurantId},
        include={"menuItems": True}
    )


# ==========================================
# MENU ITEMS
# ==========================================

@router.post("/items")
async def create_menu_item(data: MenuItemCreateSchema, user: User = Depends(get_current_user)):
    if not user.restaurantId:
        raise HTTPException(
            status_code=400, 
            detail="User is not assigned to any restaurant"
        )

    item_data: MenuItemCreateInput = {
        "name": data.name,
        "price": data.price,
        "category": {
            "connect": {"id": data.categoryId}
        },
        "restaurant": {
            "connect": {"id": user.restaurantId}
        }
    }

    if data.description:
        item_data["description"] = data.description
    if data.image:
        item_data["image"] = data.image

    item = await db.menuitem.create(data=item_data)
    return item


@router.get("/items")
async def get_menu_items(user: User = Depends(get_current_user)):
    if not user.restaurantId:
        raise HTTPException(
            status_code=400, 
            detail="User is not assigned to any restaurant"
        )

    return await db.menuitem.find_many(
        where={"restaurantId": user.restaurantId},
        include={"category": True}
    )