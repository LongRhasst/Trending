from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from sqlalchemy.orm import declarative_base

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Database session dependency"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_auth_service(db: AsyncSession):
    """AuthService dependency"""
    from app.api.v1.auth.services import AuthService
    return AuthService(db)


async def get_user_service(db: AsyncSession):
    """UserService dependency"""
    from app.api.v1.user.services import UserService
    return UserService(db)