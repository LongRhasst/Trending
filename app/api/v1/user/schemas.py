from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class SignUpSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)

class SignUpResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class SignInSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)

class SignInResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"