#middleware for authorization
from fastapi import Request, HTTPException, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.status import HTTP_401_UNAUTHORIZED
from app.core.security import verify_token

"""Paths that should be accessible without an Authorization header.

Note: frontend requests to the auth endpoints (e.g. /api/v1/auth/login)
must be allowed so CORS preflight and login requests are not blocked by
the authorization middleware. Add API prefixes used by the routers here.
"""
public_routes = [
    # "/public",
    "/docs",
    "/api/v1/openapi.json",
    "/api/v1/auth",
]

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