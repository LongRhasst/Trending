from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.user.schemas import SignUpResponseSchema, SignUpSchema
from app.api.v1.user.models import User
from app.core.security import hash_password
from sqlalchemy.future import select


class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, user_data: SignUpSchema) -> SignUpResponseSchema:
        """Create a new user with hashed password"""
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hash_password(user_data.password)
        )
        self.db_session.add(new_user)
        await self.db_session.commit()
        await self.db_session.refresh(new_user)
        return new_user
    
    async def get_user_by_email(self, email: str) -> User:
        """Get user by email address"""
        result = await self.db_session.execute(
            select(User).where(User.email == email)
        )
        return result.scalars().first()