from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.database import connect_db, disconnect_db
from app.modules.auth.router import router as auth_router
from app.modules.menu.router import router as menu_router
from app.modules.orders.router import router as orders_router
from app.modules.tables.router import router as tables_router
from app.modules.inventory.router import router as inventory_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # অ্যাপ চালু হওয়ার সময় ডাটাবেসে কানেক্ট করবে
    await connect_db()
    yield
    # অ্যাপ বন্ধ হওয়ার সময় সংযোগ বিচ্ছিন্ন করবে
    await disconnect_db()

app = FastAPI(
    title="RestoCore SaaS RMS API",
    description="Multi-tenant Restaurant Management System Backend API",
    version="1.0.0",
    lifespan=lifespan
)

# ------------------------------------------------------------------
# CORS CONFIGURATION (Next.js & Local Clients Support)
# ------------------------------------------------------------------
origins = [
    "http://localhost:3000",      # Next.js local development
    "http://127.0.0.1:3000",
    # "https://your-production-app.vercel.app"  # Deployment URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],          # GET, POST, PUT, DELETE, PATCH
    allow_headers=["*"],          # Authorization, Content-Type
)

# ------------------------------------------------------------------
# REGISTER MODULE ROUTERS
# ------------------------------------------------------------------
app.include_router(auth_router)
app.include_router(menu_router)
app.include_router(orders_router)
app.include_router(tables_router)
app.include_router(inventory_router)

# ------------------------------------------------------------------
# ROOT / HEALTH CHECK ENDPOINT
# ------------------------------------------------------------------
@app.get("/", tags=["Health Check"])
def root():
    return {
        "status": "online",
        "service": "RestoCore SaaS RMS Backend API",
        "version": "1.0.0"
    }
    
@app.get("/abir")
def abir():
    return{
        "stats":"abir is so good"
    }
    