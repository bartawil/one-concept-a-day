from fastapi import APIRouter, HTTPException, Body, Depends

from app.models.user_model import UserCreate, UserResponse, UserLogin, UserLoginResponse
from app.services.user_service import register_user, authenticate_user
from app.db.user_repository import add_interest, remove_interest
from app.middleware.auth import get_current_user
from app.services.auth_service import create_access_token

router = APIRouter()

@router.post("/users", response_model=UserLoginResponse)
async def create_user(user: UserCreate):
    try:
        new_user = await register_user(user)
        # Create JWT token for new user
        access_token = create_access_token(new_user.id, new_user.email)
        return UserLoginResponse(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email,
            interests=new_user.interests,
            access_token=access_token,
            token_type="bearer"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=UserLoginResponse)
async def login(user: UserLogin):
    authenticated_user = await authenticate_user(user)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return authenticated_user


@router.post("/user/{user_id}/interests/add")
async def add_user_interest(
    user_id: str, 
    interest: str = Body(...),
    current_user: dict = Depends(get_current_user)
):
    # Verify that the user can only modify their own data
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        await add_interest(user_id, interest)
        return {"status": "interest added"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to add interest")


@router.post("/user/{user_id}/interests/remove")
async def remove_user_interest(
    user_id: str, 
    interest: str = Body(...),
    current_user: dict = Depends(get_current_user)
):
    # Verify that the user can only modify their own data
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
        
    try:
        await remove_interest(user_id, interest)
        return {"status": "interest removed"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to remove interest")