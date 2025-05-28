from fastapi import APIRouter, HTTPException
from app.models.user_model import UserCreate, UserInDB, UserResponse, UserLogin
from app.services.user_service import register_user, get_user, authenticate_user

router = APIRouter()

@router.post("/users", response_model=UserInDB)
async def create_user(user: UserCreate):
    try:
        return await register_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/users/{email}", response_model=UserResponse)
async def read_user(email: str):
    user = await get_user(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/login", response_model=UserResponse)
async def login(user: UserLogin):
    authenticated_user = await authenticate_user(user)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return authenticated_user