from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any, cast
from app.core.database import db
from app.modules.auth.dependencies import get_current_user
from app.modules.orders.schemas import CreateOrderSchema, UpdateOrderStatusSchema
from prisma.models import User
from prisma.enums import OrderStatus
from prisma.types import (
    OrderWhereInput,
    OrderCreateInput,
    EnumOrderStatusFilter,
)

router = APIRouter(prefix="/api/v1/orders", tags=["Orders & KDS"])


@router.post("/")
async def create_order(data: CreateOrderSchema, user: User = Depends(get_current_user)):
    if not user.restaurantId:
        raise HTTPException(
            status_code=400, 
            detail="User is not assigned to any restaurant"
        )

    total_amount = 0.0
    order_items_data: List[Any] = []

    for item in data.items:
        menu_item = await db.menuitem.find_unique(where={"id": item.menuItemId})
        if not menu_item:
            raise HTTPException(
                status_code=404, 
                detail=f"Menu item {item.menuItemId} not found"
            )

        item_total = menu_item.price * item.quantity
        total_amount += item_total

        item_entry = {
            "menuItem": {"connect": {"id": menu_item.id}},
            "quantity": item.quantity,
            "unitPrice": menu_item.price,
            "totalPrice": item_total,
        }
        if item.notes:
            item_entry["notes"] = item.notes

        order_items_data.append(item_entry)

    count_where: OrderWhereInput = {
        "restaurantId": user.restaurantId
    }
    order_count = await db.order.count(where=count_where)
    order_number = f"ORD-{order_count + 1:04d}"

    order_payload: OrderCreateInput = {
        "orderNumber": order_number,
        "orderType": data.orderType,
        "totalAmount": total_amount,
        "netAmount": total_amount,
        "restaurant": {"connect": {"id": user.restaurantId}},
        "waiter": {"connect": {"id": user.id}},
        "items": {"create": order_items_data},
    }

    if data.tableId:
        order_payload["table"] = {"connect": {"id": data.tableId}}

    order = await db.order.create(
        data=order_payload,
        include={"items": True}
    )
    return order


# Kitchen Display System (KDS) Active Orders
@router.get("/kds")
async def get_kds_orders(user: User = Depends(get_current_user)):
    if not user.restaurantId:
        raise HTTPException(
            status_code=400, 
            detail="User is not assigned to any restaurant"
        )

    # EnumOrderStatusFilter ব্যবহার করে টাইপ সেফ ক্যোয়ারি
    status_filter: EnumOrderStatusFilter = {
        "in": [OrderStatus.PENDING, OrderStatus.COOKING]
    }

    kds_where: OrderWhereInput = {
        "restaurantId": user.restaurantId,
        "status": status_filter
    }

    return await db.order.find_many(
        where=kds_where,
        include={"items": {"include": {"menuItem": True}}, "table": True}
    )


@router.patch("/{order_id}/status")
async def update_order_status(
    order_id: str, 
    data: UpdateOrderStatusSchema, 
    user: User = Depends(get_current_user)
):
    if not user.restaurantId:
        raise HTTPException(
            status_code=400, 
            detail="User is not assigned to any restaurant"
        )

    existing_order = await db.order.find_first(
        where={"id": order_id, "restaurantId": user.restaurantId}
    )
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

    return await db.order.update(
        where={"id": order_id},
        data={"status": data.status}
    )