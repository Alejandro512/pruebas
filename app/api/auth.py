from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from app.core.jwt import create_access_token
from app.core.security import verify_password
from app.crud.administrator import get_administrator_by_email
from app.schemas.administrator import LoginRequest, TokenResponse
from app.services.audit import log_action

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, request: Request):
    user = await get_administrator_by_email(payload.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if user.status != "active":
        raise HTTPException(status_code=403, detail="Account is not active")

    if not await verify_password(payload.password, user.salt, user.passwordHash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": str(user.id),
        "role": user.role,
        "status": user.status,
        "isSuperAdmin": user.isSuperAdmin
    })

    await log_action(
        actor_id=user.id,
        actor_role=user.role,
        action="login",
        entity_type="administrators",
        entity_id=user.id,
        details={"email": user.email},
        ip_address=request.client.host,
        user_agent=request.headers.get("User-Agent")
    )

    return TokenResponse(access_token=token)
