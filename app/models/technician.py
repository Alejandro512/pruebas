from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from datetime import datetime

class TechnicianBase(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    phone: str

class TechnicianInDB(TechnicianBase):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    salt: str
    passwordHash: str
    role: str = "technician"
    createdAt: datetime
    status: str  # active, suspended, deleted

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
