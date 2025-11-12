from fastapi import FastAPI
from app.api.v1.auth.router import auth_router
from app.core.middleware.authorizeMiddleware import AuthorizeMiddleware
from contextlib import asynccontextmanager
from app.core.init_db import init_default_admin
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    try:
        await init_default_admin()
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
    
    yield


app = FastAPI(lifespan=lifespan)

# Add middleware
app.add_middleware(AuthorizeMiddleware)

# Add routers
app.include_router(auth_router)