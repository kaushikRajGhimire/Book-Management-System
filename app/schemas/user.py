# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    id: str

    class Config:
        schema_extra = {
            "example": {
                "id": "5f8a4d33e8b2c8f0b0f8d4c0",
                "username": "johndoe",
                "email": "john.doe@example.com"
            }
        }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None