import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings

security = HTTPBearer()

def decode_jwt(token: str) -> dict:
    """Decode and validate Supabase JWT token"""
    try:
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            options={"verify_exp": True}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    """Extract and validate user from JWT token"""
    token = credentials.credentials
    payload = decode_jwt(token)
    
    if not payload.get("sub"):
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    return {
        "id": payload.get("sub"),
        "email": payload.get("email"),
        "role": payload.get("role", "authenticated")
    }
