from app.core.database import db
from app.models.user import UserInDB
from app.core.security import hash_password
from datetime import datetime

async def create_user(data: dict) -> UserInDB:
    salt, password_hash = await hash_password(data.pop("password"))
    doc = {
        **data,
        "salt": salt,
        "passwordHash": password_hash,
        "role": "user",
        "createdAt": datetime.utcnow(),
        "status": "active"
    }
    result = await db["users"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return UserInDB(**doc)
