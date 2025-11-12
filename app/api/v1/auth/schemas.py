from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Union
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
    email: Optional[str] = None
    username: Optional[str] = None
    password: str = Field(..., min_length=8, max_length=72)
    
    @field_validator('email', mode='before')
    @classmethod
    def validate_email(cls, v):
        """Convert empty string to None, otherwise validate as email"""
        if v == "" or v is None:
            return None
        # Basic email validation
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v
    
    @field_validator('username', mode='before')
    @classmethod
    def validate_username(cls, v):
        """Convert empty string to None"""
        if v == "" or v is None:
            return None
        return v
    
    def model_post_init(self):
        """Validate that at least one of email or username is provided"""
        if not self.email and not self.username:
            raise ValueError("Either email or username must be provided")

class SignInResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"