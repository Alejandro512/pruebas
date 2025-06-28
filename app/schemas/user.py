from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    company: str
    password: str

class UserOut(BaseModel):
    id: str
    name: str
    lastname: str
    email: EmailStr
    company: str
    status: str
