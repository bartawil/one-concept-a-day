from fastapi import APIRouter, HTTPException, Body

from app.models.user_model import UserCreate, UserInDB, UserResponse, UserLogin
from app.services.user_service import register_user, authenticate_user
from app.db.user_repository import add_interest, remove_interest

router = APIRouter()

@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    try:
        new_user = await register_user(user)
        return UserResponse(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email,
            interests=new_user.interests,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=UserResponse)
async def login(user: UserLogin):
    authenticated_user = await authenticate_user(user)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return authenticated_user


@router.post("/user/{user_id}/interests/add")
async def add_user_interest(user_id: str, interest: str = Body(...)):
    await add_interest(user_id, interest)
    return {"status": "interest added"}


@router.post("/user/{user_id}/interests/remove")
async def remove_user_interest(user_id: str, interest: str = Body(...)):
    await remove_interest(user_id, interest)
    return {"status": "interest removed"}