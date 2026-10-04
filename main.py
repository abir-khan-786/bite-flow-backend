from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import connect_db, disconnect_db

from app.modules.auth.router import router as auth_router
from app.modules.menu.router import router as menu_router
from app.modules.orders.router import router as orders_router
from app.modules.tables.router import router as tables_router
from app.modules.inventory.router import router as inventory_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await disconnect_db()

app = FastAPI(title="RestoCore SaaS RMS API", version="1.0.0", lifespan=lifespan)

# Register Routers
app.include_router(auth_router)
app.include_router(menu_router)
app.include_router(orders_router)
app.include_router(tables_router)
app.include_router(inventory_router)

@app.get("/")
def root():
    return {"message": "SaaS RMS Backend API is running!"}