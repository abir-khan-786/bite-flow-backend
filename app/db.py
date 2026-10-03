from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from pydantic_settings import BaseSettings
from typing import AsyncGenerator
import os

#.env file টা backend folder এর ভিতরে আছে কিনা নিশ্চিত করা
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Settings(BaseSettings):
    CENTRAL_DB_URL: str

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = 'utf-8'
        extra = "ignore"

# এখানেই error টা দিচ্ছিলো
try:
    settings = Settings()
except Exception as e:
    print("❌.env পাওয়া যায়নি! Error:", e)
    print(f"📁 আমি খুঁজছি এইখানে: {os.path.join(BASE_DIR, '.env')}")
    raise e

def clean_url(url: str) -> str:
    url = url.strip().strip('"').strip("'")
    if url.startswith("postgresql+asyncpg://"):
        return url
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url

FINAL_URL = clean_url(settings.CENTRAL_DB_URL)

central_engine = create_async_engine(
    FINAL_URL,
    pool_pre_ping=True,
    pool_size=20,
    echo=False
)

CentralSessionLocal = async_sessionmaker(
    bind=central_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with CentralSessionLocal() as session:
        yield session

tenant_engines = {}
def get_tenant_engine(db_url: str):
    url = clean_url(db_url)
    if url in tenant_engines:
        return tenant_engines[url]
    engine = create_async_engine(url, pool_size=10)
    tenant_engines[url] = engine
    return engine