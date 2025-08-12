# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional



class UserBase(BaseModel):
    username: str
    email: EmailStr

# register
class UserCreate(UserBase):
    password: str

# login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# response
class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
    
# token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# class TokenData(BaseModel):
#     email: Optional[str] = None
