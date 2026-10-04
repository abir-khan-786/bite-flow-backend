from fastapi import APIRouter, Depends
from app.core.database import db
from app.modules.auth.dependencies import get_current_user
from app.modules.tables.schemas import TableCreateSchema, TableStatusUpdateSchema
from prisma.models import User

router = APIRouter(prefix="/api/v1/tables", tags=["Tables"])

@router.post("/")
async def create_table(data: TableCreateSchema, user: User = Depends(get_current_user)):
    return await db.table.create(
        data={
            "tableNumber": data.tableNumber,
            "capacity": data.capacity,
            "restaurantId": user.restaurantId
        }
    )

@router.get("/")
async def get_tables(user: User = Depends(get_current_user)):
    return await db.table.find_many(where={"restaurantId": user.restaurantId})

@router.patch("/{table_id}/status")
async def update_table_status(table_id: str, data: TableStatusUpdateSchema, user: User = Depends(get_current_user)):
    return await db.table.update(
        where={"id": table_id},
        data={"status": data.status}
    )