# pyright: reportUndefinedVariable=false

from app.db.mongodb import db
from app.models.user_model import UserCreate, UserInDB
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
import bcrypt


# Create a new user in the database
async def create_user(user: UserCreate) -> UserInDB:
    user_data = user.model_dump()

    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(user_data["password"].encode('utf-8'), bcrypt.gensalt())
    user_data["password"] = hashed_password.decode('utf-8')  # Store as string
    
    result = await db["users"].insert_one(user_data)
    return UserInDB(id=str(result.inserted_id), **user_data)


# Find a user by email (for login or validation)
async def get_user_by_email(email: str) -> UserInDB | None:
    user_data = await db["users"].find_one({"email": email})
    if user_data:
        return UserInDB(id=str(user_data["_id"]), **user_data)
    return None


# Optional: Find a user by ID
async def get_user_by_id(user_id: str) -> UserInDB | None:
    user_data = await db["users"].find_one({"_id": ObjectId(user_id)})
    if user_data:
        return UserInDB(id=str(user_data["_id"]), **user_data)
    return None
