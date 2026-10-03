from fastapi import FastAPI
from sqlalchemy import text
from app.db import central_engine

app = FastAPI(
    title="Bite-Flow API",
    version="1.0"
)

@app.get("/")
async def root():
    return {"message": "Bite-Flow Backend Running 🔥"}

@app.get("/health/db")
async def database_health():
    try:
        async with central_engine.connect() as connection:
            await connection.execute(text("SELECT 1"))

        return {
            "status": "success",
            "database": "PostgreSQL connected"
        }

    except Exception as e:
        return {
            "status": "error",
            "database": "PostgreSQL not connected",
            "error": str(e)
        }

# তোর আগের /health টাও রাখলাম যাতে 404 না আসে
@app.get("/health")
async def health():
    return await database_health()