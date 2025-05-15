from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    interests: Optional[list[str]] = []

class UserInDB(UserCreate):
    id: str
