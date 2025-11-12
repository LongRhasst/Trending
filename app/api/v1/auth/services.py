from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.user.services import UserService
from app.api.v1.auth.repository import AuthRepository
from app.api.v1.user.schemas import SignInSchema, SignUpSchema, SignInResponseSchema, SignUpResponseSchema
from app.core.security import verify_password, create_access_token


class AuthService:
    
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.user_service = UserService(db_session)
        self.auth_repository = AuthRepository(db_session)

    async def login_user(self, login_data: SignInSchema) -> SignInResponseSchema:
        """Authenticate user and return access token"""
        # Get user by email
        user = await self.user_service.get_user_by_email(login_data.email)
        
        if not user or not verify_password(login_data.password, user.hashed_password):
            return None
        
        # Create access token
        access_token = create_access_token(data={"sub": user.email})
        
        return SignInResponseSchema(
            access_token=access_token,
            token_type="bearer"
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