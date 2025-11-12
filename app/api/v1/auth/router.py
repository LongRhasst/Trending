from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.auth.services import AuthService
from app.api.v1.user.schemas import SignInResponseSchema, SignInSchema, SignUpSchema, SignUpResponseSchema
from app.api.Dependences import get_db

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@auth_router.post("/login", response_model=SignInResponseSchema)
async def login(
    sign_in_data: SignInSchema,
    db: AsyncSession = Depends(get_db)
):
    """Login endpoint"""
    auth_service = AuthService(db)
    result = await auth_service.login_user(sign_in_data)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return result


@auth_router.post("/register", response_model=SignUpResponseSchema)
async def register(
    user_data: SignUpSchema,
    db: AsyncSession = Depends(get_db)
):
    """Register endpoint"""
    auth_service = AuthService(db)
    result = await auth_service.register_user(user_data)
    return result