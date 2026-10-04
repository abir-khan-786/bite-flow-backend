from prisma import Prisma

# গ্লোবাল প্রিসমা ইনস্ট্যান্স
db = Prisma()

async def connect_db():
    if not db.is_connected():
        await db.connect()
        print("✅ Database connected successfully!")

async def disconnect_db():
    if db.is_connected():
        await db.disconnect()
        print("🔌 Database disconnected.")