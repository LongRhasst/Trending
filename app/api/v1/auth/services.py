import hashlib
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.user.services import UserService
from app.api.v1.auth.repository import AuthRepository
from app.api.v1.auth.schemas import SignInSchema, SignUpSchema, SignInResponseSchema, SignUpResponseSchema
from app.core.security import create_refresh_token, verify_password, create_access_token


class AuthService:
    
    def __init__(self, db: AsyncSession):
        """
        Initialize service with database session.
        Session is injected and passed to both user_service and auth_repository.
        """
        self.db = db
        self.user_service = UserService(db)
        self.auth_repository = AuthRepository(db)

    async def refresh_access_token(self, refresh_token: str) -> SignInResponseSchema:
        """
        Validate refresh token and create new access token.
        The old refresh token is revoked (token rotation).
        """
        # Hash the provided token
        refresh_token_hashed = hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()
        
        # Get user by refresh token and revoke old token
        user = await self.auth_repository.get_user_by_refresh_token(refresh_token_hashed)
        
        if not user:
            return None

        # Create new access token
        access_token = create_access_token(data={
            "sub": user.email,
            "username": user.username,
            "user_id": user.id
        })
        
        # Create new refresh token
        new_refresh_token = await create_refresh_token(
            data={"user_id": user.id}
        )
        
        return SignInResponseSchema(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
        )

    async def login_user(self, login_data: SignInSchema) -> SignInResponseSchema:
        """Authenticate user and return access token"""
        # Get user by email or username
        user = await self.user_service.user_repository.get_user_by_email_or_username(
            email=login_data.email,
            username=login_data.username
        )
        
        if not user or not verify_password(login_data.password, user.hashed_password):
            return None
        
        # Create access token with user's email and username
        access_token = create_access_token(data={
            "sub": user.email,
            "username": user.username,
            "user_id": user.id
        })
        
        # Create and persist refresh token
        raw_refresh_token = await create_refresh_token(
            data={"user_id": user.id}
        )

        return SignInResponseSchema(
            access_token=access_token,
            refresh_token=raw_refresh_token,
            token_type="bearer",
        )

    async def register_user(self, user_data: SignUpSchema) -> SignUpResponseSchema:
        """Register new user"""
        # Check if user already exists
        existing_user = await self.user_service.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Create new user
        result = await self.user_service.user_repository.create_user(user_data)
        return result