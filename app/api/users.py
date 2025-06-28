from fastapi import APIRouter, Depends, Request, HTTPException
from app.schemas.user import UserCreate, UserOut
from app.crud.user import create_user
from app.services.audit import log_action
from app.core.deps import get_current_admin

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
    return UserOut(
        id=str(new_user.id),
        name=new_user.name,
        lastname=new_user.lastname,
        email=new_user.email,
        company=new_user.company,
        status=new_user.status
    )
