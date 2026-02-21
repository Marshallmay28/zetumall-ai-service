from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request
from app.config import settings

class ApiKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Allow health checks and docs without auth
        if request.url.path in ["/health", "/", "/docs", "/openapi.json"]:
            return await call_next(request)

        api_key = request.headers.get("X-API-KEY")
        
        # In production, use a secure comparison to prevent timing attacks
        # For this MVP, direct comparison is acceptable but we should use the env var
        expected_key = settings.ai_service_api_key if hasattr(settings, 'ai_service_api_key') else "zetumall_ai_secret_key_123"

        if not api_key or api_key != expected_key:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or missing API Key"}
            )

        return await call_next(request)

async def verify_api_key(request: Request):
    api_key = request.headers.get("X-API-KEY")
    expected_key = settings.ai_service_api_key if hasattr(settings, 'ai_service_api_key') else "zetumall_ai_secret_key_123"
    
    if not api_key or api_key != expected_key:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")
    return api_key
