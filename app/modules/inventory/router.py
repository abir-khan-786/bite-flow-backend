from fastapi import APIRouter, Depends
from app.core.database import db
from app.modules.auth.dependencies import get_current_user
from app.modules.inventory.schemas import InventoryCreateSchema, InventoryUpdateStockSchema
from prisma.models import User

router = APIRouter(prefix="/api/v1/inventory", tags=["Inventory"])

@router.post("/")
async def add_inventory_item(data: InventoryCreateSchema, user: User = Depends(get_current_user)):
    return await db.inventory.create(
        data={
            "itemName": data.itemName,
            "quantity": data.quantity,
            "unit": data.unit,
            "minThreshold": data.minThreshold,
            "restaurantId": user.restaurantId
        }
    )

@router.get("/")
async def get_inventory(user: User = Depends(get_current_user)):
    return await db.inventory.find_many(where={"restaurantId": user.restaurantId})

@router.patch("/{item_id}/stock")
async def update_stock(item_id: str, data: InventoryUpdateStockSchema, user: User = Depends(get_current_user)):
    return await db.inventory.update(
        where={"id": item_id},
        data={"quantity": data.quantity}
    )