from fastapi import APIRouter, HTTPException
from app.models.user_model import UserLogin, UserResponse
from app.services.user_service import authenticate_user

router = APIRouter()

@router.post("/auth/login", response_model=UserResponse)
async def login_user(login_data: UserLogin):
    user = await authenticate_user(login_data)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return user
