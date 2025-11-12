from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.user.repository import UserRepository


class UserService:

    def __init__(self, db: AsyncSession):
        """
        Initialize service with database session.
        Session is injected and passed to repository.
        """
        self.db = db
        self.user_repository = UserRepository(db)

    async def get_user_by_email(self, email: str):
        """Get user by email"""
        return await self.user_repository.get_user_by_email(email)