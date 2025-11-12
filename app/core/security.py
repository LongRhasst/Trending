from datetime import datetime, timedelta
from typing import Optional
import secrets
import hashlib
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from jose import JWTError, jwt
from app.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = getattr(settings, 'SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def _truncate_password(password: str, max_bytes: int = 72) -> str:
    """
    Truncate password to maximum bytes for bcrypt compatibility.
    Bcrypt has a maximum password length of 72 bytes.
    """
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > max_bytes:
        # Truncate to max_bytes and decode, ignoring errors at the boundary
        password_bytes = password_bytes[:max_bytes]
        password = password_bytes.decode('utf-8', errors='ignore')
    return password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    # Apply same truncation as hash_password for consistency
    plain_password = _truncate_password(plain_password)
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """Hash a password"""
    # Truncate password to 72 bytes if necessary (bcrypt limitation)
    password = _truncate_password(password)
    return pwd_context.hash(password)

def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token and return the payload or None if invalid"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def create_refresh_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
    user_agent: Optional[str] = None,
    ip: Optional[str] = None,
) -> str:
    from app.core.database import AsyncSessionLocal
    
    # Generate a secure random token (64 bytes -> 128 hex chars to match previous length)
    refresh_token_raw = secrets.token_hex(64)

    # Hash the token before storing
    refresh_token_hash = hashlib.sha256(refresh_token_raw.encode("utf-8")).hexdigest()

    expires_at = datetime.utcnow() + (expires_delta if expires_delta else timedelta(days=30))

    # Lazy import of model to avoid circular imports at module import time
    from app.api.v1.auth.models import refreshToken as RefreshTokenModel

    # Create and persist the refresh token record with own session
    async with AsyncSessionLocal() as db_session:
        new_token = RefreshTokenModel(
            user_id=data.get("user_id"),
            token_hash=refresh_token_hash,
            expires_at=expires_at,
            revoked=False,
            user_agent=user_agent,
            ip=ip,
        )
        db_session.add(new_token)
        await db_session.commit()
        await db_session.refresh(new_token)

    return refresh_token_raw

def decode_access_token(token: str) -> Optional[dict]:
    """Decode JWT access token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None