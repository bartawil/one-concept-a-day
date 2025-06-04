from pydantic import BaseModel, EmailStr, Field
from typing import Dict, Optional, List


# Model for creating a new user
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: Optional[str] = None
    interests: Optional[List[str]] = Field(default_factory=list)



# Model for login request
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Internal DB model
class UserInDB(UserCreate):
    id: str
    history: Optional[Dict[str, List[str]]] = Field(default_factory=dict)


# Response model for frontend (no password)
class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    interests: Optional[List[str]] = []
