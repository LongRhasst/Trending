#middleware for authorization
from fastapi import Request, HTTPException, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.status import HTTP_401_UNAUTHORIZED
from app.core.security import verify_token

public_routes = ["/public", "/docs", "/openapi.json", "/auth"]

class AuthorizeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        path = request.url.path

        print( f"AuthorizeMiddleware: Processing request for path: {path}" )
        if any(path.startswith(route) for route in public_routes):
            return await call_next(request)
        
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Authorization token missing"
            )
        
        # Remove 'Bearer ' prefix if present
        if token.startswith("Bearer "):
            token = token[7:]
        
        payload = verify_token(token)
        if not payload:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        response = await call_next(request)
        return response