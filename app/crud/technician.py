from app.core.database import db
from app.models.technician import TechnicianInDB
from app.core.security import hash_password
from datetime import datetime

async def create_technician(data: dict) -> TechnicianInDB:
    salt, password_hash = await hash_password(data.pop("password"))
    doc = {
        **data,
        "salt": salt,
        "passwordHash": password_hash,
        "role": "technician",
        "createdAt": datetime.utcnow(),
        "status": "active"
    }
    result = await db["technicians"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return TechnicianInDB(**doc)
