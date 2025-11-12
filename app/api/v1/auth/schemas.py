from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)

class LoginResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"