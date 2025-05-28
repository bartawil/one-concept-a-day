import bcrypt
from app.models.user_model import UserCreate, UserInDB, UserLogin, UserResponse
from app.db.user_repository import get_user_by_email, create_user

# Business logic: register a new user if they don't already exist
async def register_user(user_data: UserCreate) -> UserInDB:
    existing_user = await get_user_by_email(user_data.email)
    if existing_user:
        raise ValueError("User already exists with this email")
    return await create_user(user_data)


# Business logic: get a user by email
async def get_user(email: str) -> UserInDB | None:
    return await get_user_by_email(email)


# Business logic: authenticate user by email and password
async def login_user(login_data: UserLogin) -> UserInDB:
    user = await get_user_by_email(login_data.email)
    if not user or not bcrypt.checkpw(login_data.password.encode(), user.password.encode()):
        raise ValueError("Invalid email or password")
    return user


# Authenticate user and return public data
async def authenticate_user(login_data: UserLogin) -> UserResponse | None:
    user = await get_user_by_email(login_data.email)
    if not user or not bcrypt.checkpw(login_data.password.encode(), user.password.encode()):
        return None
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        interests=user.interests
    )
