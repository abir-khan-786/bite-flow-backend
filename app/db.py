import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator

#.env load - 100% guaranteed
# backend/.env আর backend/app/db.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

print(f"🔍.env Path is her: {ENV_PATH}")
print(f"📄.env Her Database? {os.path.exists(ENV_PATH)}")

CENTRAL_DB_URL_RAW = os.getenv("CENTRAL_DB_URL")

if not CENTRAL_DB_URL_RAW:
    print("❌ CENTRAL_DB_URL পাওয়া যায়নি.env তে!")
    print("📂.env file এর ভিতরের content:")
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, 'r') as f:
            print(f.read())
    raise ValueError("CENTRAL_DB_URL is missing in.env")

def clean_url(url: str) -> str:
    url = url.strip().strip('"').strip("'")
    url = url.replace("?sslmode=require&channel_binding=require", "?ssl=require")
    url = url.replace("?sslmode=require", "?ssl=require")
    url = url.replace("&sslmode=require", "")
    url = url.replace("&channel_binding=require", "")
    url = url.replace("channel_binding=require", "")
    if "?" in url and url.endswith("?"):
        url = url[:-1]

    if url.startswith("postgresql+asyncpg://"):
        return url
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url

FINAL_URL = clean_url(CENTRAL_DB_URL_RAW)
print(f"✅ DB URL Loaded: {FINAL_URL[:40]}...")

central_engine = create_async_engine(
    FINAL_URL,
    pool_pre_ping=True,
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