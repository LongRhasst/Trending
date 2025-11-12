from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.user.models import User
from app.api.v1.auth.models import refreshToken as RefreshTokenModel
from datetime import datetime, timezone


class AuthRepository:
    def __init__(self, db: AsyncSession):
        """
        Initialize repository with database session.
        Session is injected via dependency injection.
        """
        self.db = db

    async def authorize_user(self, email: str, hashed_password: str):
        """Authorize user by email and hashed password"""
        result = await self.db.execute(
            select(User).where(User.email == email, User.hashed_password == hashed_password)
        )
        return result.scalars().first()
    
    async def get_user_by_refresh_token(self, refresh_token_hashed: str):
        """
        Get user by refresh token hash and revoke the token.
        Returns None if token is invalid, revoked, or expired.
        """
        # Look up token in refresh_tokens table
        result = await self.db.execute(
            select(RefreshTokenModel).where(
                RefreshTokenModel.token_hash == refresh_token_hashed
            )
        )
        token_record = result.scalars().first()
        
        if not token_record:
            return None
        
        # Check if token is revoked
        if token_record.revoked:
            return None
        
        # Check if token is expired (use timezone-aware datetime)
        now = datetime.now(timezone.utc)
        if token_record.expires_at < now:
            return None
        
        # Revoke the old refresh token (rotation)
        await self.db.execute(
            update(RefreshTokenModel)
            .where(RefreshTokenModel.id == token_record.id)
            .values(revoked=True)
        )
        await self.db.commit()
        
        # Get the user
        result = await self.db.execute(
            select(User).where(User.id == token_record.user_id)
        )
        return result.scalars().first()