from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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


app = FastAPI(
    lifespan=lifespan,
    root_path="/api/v1"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default port
        "http://localhost:3000",  # React default port
        "http://localhost:8080",  # Vue default port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Add custom middleware
app.add_middleware(AuthorizeMiddleware)

# Add routers
app.include_router(auth_router)