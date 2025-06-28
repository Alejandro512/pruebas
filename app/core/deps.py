from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

security = HTTPBearer()

async def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        if payload["role"] != "administrator":
            raise HTTPException(status_code=403, detail="Not authorized")
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")

async def get_current_superadmin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    admin = await get_current_admin(credentials)
    if not admin.get("isSuperAdmin", False):
        raise HTTPException(status_code=403, detail="Not superadmin")
    return admin
