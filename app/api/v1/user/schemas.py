from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class SignUpSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

class SignUpResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class SignInSchema(BaseModel):
    email: EmailStr
    password: str

class SignInResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"