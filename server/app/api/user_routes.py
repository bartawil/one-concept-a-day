from fastapi import APIRouter, HTTPException
from app.models.user_model import UserCreate
from app.services.user_service import create_user, get_user_by_email

router = APIRouter()

@router.post("/users")
async def register_user(user: UserCreate):
    existing = await get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    user_id = await create_user(user)
    return {"message": "User created successfully", "user_id": user_id}
