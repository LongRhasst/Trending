from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "password"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: str = "5432"
    DATABASE_NAME: str = "boxchat_db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Default admin user
    username: str = "admin"
    password: str = "admin123"
    email: str = "admin@example.com"
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"  # Ignore extra fields from .env
    )


settings = Settings()