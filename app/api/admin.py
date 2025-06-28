from fastapi import APIRouter, Depends, HTTPException, Request, Path
from app.schemas.administrator import AdministratorCreate, AdministratorOut
from app.crud.administrator import create_administrator
from app.services.audit import log_action
from app.core.database import db
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

router = APIRouter(prefix="/admin", tags=["administrators"])

security = HTTPBearer()

async def get_current_superadmin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        if not payload.get("isSuperAdmin", False):
            raise HTTPException(status_code=403, detail="Not authorized")
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")

@router.post("/create", response_model=AdministratorOut)
async def create_admin(data: AdministratorCreate, request: Request, superadmin=Depends(get_current_superadmin)):
    new_admin = await create_administrator(data.dict())
    await log_action(
        actor_id=superadmin["sub"],
        actor_role=superadmin["role"],
        action="create_administrator",
        entity_type="administrators",
        entity_id=new_admin.id,
        details={"created_email": new_admin.email},
        ip_address=request.client.host,
        user_agent=request.headers.get("User-Agent")
    )
    return new_admin

@router.patch("/{id}/status")
async def update_admin_status(
    id: str,
    status: str,
    request: Request,
    superadmin=Depends(get_current_superadmin)
):
    if status not in ["active", "suspended", "deleted"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    result = await db["administrators"].update_one(
        {"_id": id}, {"$set": {"status": status}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Admin not found")

    await log_action(
        actor_id=superadmin["sub"],
        actor_role=superadmin["role"],
        action="update_admin_status",
        entity_type="administrators",
        entity_id=id,
        details={"new_status": status},
        ip_address=request.client.host,
        user_agent=request.headers.get("User-Agent")
    )
    return {"message": f"Status updated to {status}"}