from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from datetime import datetime

class AdministratorBase(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    isSuperAdmin: bool = False

class AdministratorInDB(AdministratorBase):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    salt: str
    passwordHash: str
    role: str = "administrator"
    createdAt: datetime
    status: str  # active, suspended, deleted

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
