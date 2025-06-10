import bcrypt
from app.models.user_model import UserCreate, UserInDB, UserLogin, UserResponse, UserLoginResponse
from app.db.user_repository import get_user_by_email, create_user
from app.services.auth_service import create_access_token

# Business logic: register a new user if they don't already exist
async def register_user(user_data: UserCreate) -> UserInDB:
    existing_user = await get_user_by_email(user_data.email)
    if existing_user:
        raise ValueError("User already exists with this email")
    return await create_user(user_data)


# Authenticate user and return public data with JWT token
async def authenticate_user(login_data: UserLogin) -> UserLoginResponse | None:
    user = await get_user_by_email(login_data.email)
    if not user or not bcrypt.checkpw(login_data.password.encode(), user.password.encode()):
        return None
    
    # Create JWT token
    access_token = create_access_token(user.id, user.email)
    
    return UserLoginResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        interests=user.interests,
        access_token=access_token,
        token_type="bearer"
    )
