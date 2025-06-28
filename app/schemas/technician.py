from pydantic import BaseModel, EmailStr

class TechnicianCreate(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    phone: str
    password: str

class TechnicianOut(BaseModel):
    id: str
    name: str
    lastname: str
    email: EmailStr
    phone: str
    status: str
