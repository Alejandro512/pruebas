from fastapi import APIRouter, Depends, Request, HTTPException
from schemas.technician import TechnicianCreate, TechnicianOut
from crud.technician import create_technician
from services.audit import log_action
from core.deps import get_current_admin

router = APIRouter(prefix="/technicians", tags=["technicians"])

@router.post("/create", response_model=TechnicianOut)
async def create_tech(data: TechnicianCreate, request: Request, admin=Depends(get_current_admin)):
    new_tech = await create_technician(data.dict())
    await log_action(
        actor_id=admin["sub"],
        actor_role=admin["role"],
        action="create_technician",
        entity_type="technicians",
        entity_id=new_tech.id,
        details={"created_email": new_tech.email},
        ip_address=request.client.host,
        user_agent=request.headers.get("User-Agent")
    )
    return new_tech
