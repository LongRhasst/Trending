from sqlalchemy import select
from app.api.v1.user.models import User
class AuthRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    async def authorize_user(self, email: str, hashed_password: str):
        result = await self.db_session.execute(
            select(User).where(User.email == email, User.hashed_password == hashed_password)
        )
        return result.scalars().first()