from app.models.user_model import UserCreate
from app.db.mongodb import db
from bson.objectid import ObjectId

async def create_user(user_data: UserCreate) -> str:
    user_dict = user_data.dict()
    result = await db["users"].insert_one(user_dict)
    return str(result.inserted_id)

async def get_user_by_email(email: str):
    user = await db["users"].find_one({"email": email})
    if user:
        user["id"] = str(user["_id"])
        del user["_id"]
    return user
