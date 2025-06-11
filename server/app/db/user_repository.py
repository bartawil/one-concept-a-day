# pyright: reportUndefinedVariable=false

from app.db.mongodb import db
from app.models.user_model import UserCreate, UserInDB
from app.security.security import sanitize_string_input, sanitize_html_content, validate_object_id
from bson import ObjectId
import bcrypt
from datetime import datetime, timezone


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
    try:
        object_id = validate_object_id(user_id)
        user_data = await db["users"].find_one({"_id": object_id})
        if user_data:
            return UserInDB(id=str(user_data["_id"]), **user_data)
        return None
    except ValueError:
        return None



# Update user's history by adding a new term under a specific category
async def add_term_to_history(user_id: str, category: str, term: str):
    # Sanitize all inputs
    sanitized_category = sanitize_string_input(category, max_length=50)
    sanitized_term = sanitize_html_content(term, max_length=200)
    object_id = validate_object_id(user_id)
    
    await db["users"].update_one(
        {"_id": object_id},
        {
            "$addToSet": {f"history.{sanitized_category}": sanitized_term}
        }
    )
    

async def save_daily_concept(user_id: str, category: str, term: str, explanation: str):
    # Sanitize all inputs
    sanitized_category = sanitize_string_input(category, max_length=50)
    sanitized_term = sanitize_html_content(term, max_length=200)
    sanitized_explanation = sanitize_html_content(explanation, max_length=2000)
    object_id = validate_object_id(user_id)
    
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    await db["users"].update_one(
        {"_id": object_id},
        {
            "$set": {
                "daily": {
                    today: {
                        "category": sanitized_category,
                        "term": sanitized_term,
                        "explanation": sanitized_explanation
                    }
                }
            }
        }
    )



async def add_interest(user_id: str, interest: str):
    # Validate and sanitize inputs
    sanitized_interest = sanitize_string_input(interest, max_length=50)
    object_id = validate_object_id(user_id)
    
    # Check if user exists first
    user = await get_user_by_id(user_id)
    if not user:
        raise ValueError("User not found")
    
    await db["users"].update_one(
        {"_id": object_id},
        {"$addToSet": {"interests": sanitized_interest}}
    )

async def remove_interest(user_id: str, interest: str):
    # Validate and sanitize inputs
    sanitized_interest = sanitize_string_input(interest, max_length=50)
    object_id = validate_object_id(user_id)
    
    # Check if user exists first
    user = await get_user_by_id(user_id)
    if not user:
        raise ValueError("User not found")
        
    await db["users"].update_one(
        {"_id": object_id},
        {"$pull": {"interests": sanitized_interest}}
    )