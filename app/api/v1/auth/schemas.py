from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class LoginResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"