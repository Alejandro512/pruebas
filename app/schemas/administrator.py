from pydantic import BaseModel, EmailStr

class AdministratorCreate(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    password: str
    isSuperAdmin: bool = False

class AdministratorOut(BaseModel):
    id: str
    name: str
    lastname: str
    email: EmailStr
    isSuperAdmin: bool
    status: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
