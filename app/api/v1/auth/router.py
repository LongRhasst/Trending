from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.auth.services import AuthService
from app.api.v1.auth.schemas import (
    SignInResponseSchema,
    SignInSchema,
    SignUpSchema,
    SignUpResponseSchema,
    RefreshTokenSchema,
)
from app.api.Dependences import get_db


class AuthRouter:
    """Class-based router for auth endpoints.

    Database sessions are injected via dependency injection from get_db().
    The session flows: Router -> Service -> Repository
    """

    def __init__(self) -> None:
        self.router = APIRouter(prefix="/auth", tags=["Authentication"])
        # Register routes
        self.router.post("/login", response_model=SignInResponseSchema)(self.login)
        self.router.post("/refresh", response_model=SignInResponseSchema)(self.rotate_refresh_token)
        self.router.post("/register", response_model=SignUpResponseSchema)(self.register)

    async def login(self, sign_in_data: SignInSchema, db: AsyncSession = Depends(get_db)):
        """Login endpoint - can use email or username"""
        try:
            auth_service = AuthService(db)
            result = await auth_service.login_user(sign_in_data)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials",
                )

            return result
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def rotate_refresh_token(
        self, 
        refresh_data: RefreshTokenSchema, 
        db: AsyncSession = Depends(get_db)
    ):
        """
        Refresh token rotation endpoint.
        Validates the refresh token, revokes it, and issues new access + refresh tokens.
        """
        try:
            auth_service = AuthService(db)
            result = await auth_service.refresh_access_token(refresh_token=refresh_data.refresh_token)
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Invalid or expired refresh token"
                )
            
            return result
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred during token refresh: {str(e)}"
            )

    async def register(self, user_data: SignUpSchema, db: AsyncSession = Depends(get_db)):
        """Register endpoint"""
        try:
            auth_service = AuthService(db)
            result = await auth_service.register_user(user_data)
            return result
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred during registration: {str(e)}",
            )


# expose router instance for app to include
auth_router = AuthRouter().router