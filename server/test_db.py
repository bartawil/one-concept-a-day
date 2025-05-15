import asyncio
from app.db.mongodb import db

async def test_connection():
    try:
        # ננסה להדפיס את רשימת הקולקשנים במסד
        collections = await db.list_collection_names()
        print("✅ Connected to MongoDB successfully!")
        print("Collections:", collections)
    except Exception as e:
        print("❌ Failed to connect to MongoDB:", e)

asyncio.run(test_connection())
