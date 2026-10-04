from fastapi import APIRouter, Depends, HTTPException
from app.core.database import db
from app.modules.auth.dependencies import get_current_user
from app.modules.orders.schemas import CreateOrderSchema, UpdateOrderStatusSchema
from prisma.models import User
from prisma.enums import OrderStatus

router = APIRouter(prefix="/api/v1/orders", tags=["Orders & KDS"])

@router.post("/")
async def create_order(data: CreateOrderSchema, user: User = Depends(get_current_user)):
    total_amount = 0.0
    order_items_data = []

    for item in data.items:
        menu_item = await db.menuitem.find_unique(where={"id": item.menuItemId})
        if not menu_item:
            raise HTTPException(status_code=404, detail=f"Menu item {item.menuItemId} not found")
        
        item_total = menu_item.price * item.quantity
        total_amount += item_total
        
        order_items_data.append({
            "menuItemId": menu_item.id,
            "quantity": item.quantity,
            "unitPrice": menu_item.price,
            "totalPrice": item_total,
            "notes": item.notes
        })

    order_count = await db.order.count(where={"restaurantId": user.restaurantId})
    order_number = f"ORD-{order_count + 1:04d}"

    order = await db.order.create(
        data={
            "orderNumber": order_number,
            "orderType": data.orderType,
            "tableId": data.tableId,
            "totalAmount": total_amount,
            "netAmount": total_amount,
            "waiterId": user.id,
            "restaurantId": user.restaurantId,
            "items": {"create": order_items_data}
        },
        include={"items": True}
    )
    return order

# Kitchen Display System (KDS) Active Orders
@router.get("/kds")
async def get_kds_orders(user: User = Depends(get_current_user)):
    return await db.order.find_many(
        where={
            "restaurantId": user.restaurantId,
            "status": {"in": [OrderStatus.PENDING, OrderStatus.COOKING]}
        },
        include={"items": {"include": {"menuItem": True}}, "table": True}
    )

@router.patch("/{order_id}/status")
async def update_order_status(order_id: str, data: UpdateOrderStatusSchema, user: User = Depends(get_current_user)):
    return await db.order.update(
        where={"id": order_id},
        data={"status": data.status}
    )