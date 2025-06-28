from fastapi import APIRouter, Depends, Request, HTTPException
from schemas.user import UserCreate, UserOut
from crud.user import create_user
from services.audit import log_action
from core.deps import get_current_admin

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/create", response_model=UserOut)
async def create_user_endpoint(data: UserCreate, request: Request, admin=Depends(get_current_admin)):
    new_user = await create_user(data.dict())
    await log_action(
        actor_id=admin["sub"],
        actor_role=admin["role"],
        action="create_user",
        entity_type="users",
        entity_id=new_user.id,
        details={"created_email": new_user.email},
        ip_address=request.client.host,
        user_agent=request.headers.get("User-Agent")
    )
    return new_user
