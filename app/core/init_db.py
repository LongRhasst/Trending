"""
Database initialization script
Creates default admin user on first run
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api.v1.user.models import User
from app.core.security import hash_password
from app.core.config import settings
from app.core.database import AsyncSessionLocal
import logging

logger = logging.getLogger(__name__)


async def init_default_admin():
    """Initialize default admin user if not exists"""
    async with AsyncSessionLocal() as db:
        try:
            # Check if admin user already exists
            result = await db.execute(
                select(User).where(User.email == settings.email)
            )
            existing_user = result.scalars().first()
            
            if existing_user:
                return
            
            # Create default admin user
            admin_user = User(
                username=settings.username,
                email=settings.email,
                hashed_password=hash_password(settings.password)
            )
            
            db.add(admin_user)
            await db.commit()
            await db.refresh(admin_user)
            
            logger.info(f"Default admin user created successfully!")
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to create default admin user: {str(e)}")
            raise
        finally:
            await db.close()
