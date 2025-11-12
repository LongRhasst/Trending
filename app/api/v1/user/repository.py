from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.user.schemas import SignUpResponseSchema, SignUpSchema
from app.api.v1.user.models import User
from app.core.security import hash_password
from sqlalchemy.future import select


class UserRepository:
    def __init__(self, db: AsyncSession):
        """
        Initialize repository with database session.
        Session is injected via dependency injection.
        """
        self.db = db

    async def create_user(self, user_data: SignUpSchema) -> SignUpResponseSchema:
        """Create a new user with hashed password"""
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hash_password(user_data.password)
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        
        # Return proper response schema
        return SignUpResponseSchema(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email,
            created_at=new_user.created_at
        )
    
    async def get_user_by_email(self, email: str) -> User:
        """Get user by email address"""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalars().first()
    
    async def get_user_by_username(self, username: str) -> User:
        """Get user by username"""
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalars().first()
    
    async def get_user_by_email_or_username(self, email: str = None, username: str = None) -> User:
        """Get user by email or username"""
        if email:
            result = await self.db.execute(
                select(User).where(User.email == email)
            )
            user = result.scalars().first()
            if user:
                return user
        
        if username:
            result = await self.db.execute(
                select(User).where(User.username == username)
            )
            return result.scalars().first()
        
        return None