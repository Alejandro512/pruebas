from models.administrator import AdministratorInDB
from core.security import hash_password
from app.core.database import db
from datetime import datetime

async def create_administrator(admin_data: dict) -> AdministratorInDB:
    salt, password_hash = await hash_password(admin_data.pop("password"))
    admin_doc = {
        **admin_data,
        "salt": salt,
        "passwordHash": password_hash,
        "role": "administrator",
        "createdAt": datetime.utcnow(),
        "status": "active"
    }
    result = await db["administrators"].insert_one(admin_doc)
    admin_doc["_id"] = result.inserted_id
    return AdministratorInDB(**admin_doc)

async def get_administrator_by_email(email: str) -> AdministratorInDB | None:
    data = await db["administrators"].find_one({"email": email})
    if data:
        return AdministratorInDB(**data)
    return None
