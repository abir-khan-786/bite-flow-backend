from fastapi import APIRouter, Depends
from app.api.deps import get_current_restaurant, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

router = APIRouter()

@router.get("/")
async def list_orders(
    tenant_engine = Depends(get_current_restaurant),
    user = Depends(get_current_user)
):
    async with AsyncSession(tenant_engine) as session:
        result = await session.execute(text("SELECT * FROM orders ORDER BY created_at DESC LIMIT 50"))
        return result.mappings().all()

@router.post("/")
async def create_order(data: dict, tenant_engine = Depends(get_current_restaurant)):
    # Public route - QR menu থেকে আসবে, auth লাগবে না
    async with AsyncSession(tenant_engine) as session:
        await session.execute(text("INSERT INTO orders (id, items, total) VALUES (gen_random_uuid(), :items, :total)"),
                              {"items": str(data['items']), "total": data['total']})
        await session.commit()
        return {"status": "success"}