from fastapi import FastAPI
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from app.db import central_engine, Base
from app.routers import restaurant
# User import of 
app = FastAPI(title="Bite-Flow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

@app.on_event("startup")
async def on_startup():
    async with central_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created")

app.include_router(restaurant.router)

@app.get("/")
async def root():
    return {"message": "Bite-Flow API is running"}