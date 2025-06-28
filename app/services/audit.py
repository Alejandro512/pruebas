from app.core.database import db
from datetime import datetime

async def log_action(actor_id, actor_role, action, entity_type, entity_id, details, ip_address, user_agent):
    log_doc = {
        "actorId": actor_id,
        "actorRole": actor_role,
        "action": action,
        "entityType": entity_type,
        "entityId": entity_id,
        "details": details,
        "ipAddress": ip_address,
        "userAgent": user_agent,
        "createdAt": datetime.utcnow()
    }
    await db["auditLogs"].insert_one(log_doc)
