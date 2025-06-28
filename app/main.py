from fastapi import FastAPI
from app.core.rate_limit import register_rate_limit_handler, limiter
from app.api import auth, admin, technicians, users

app = FastAPI(
    title="Laboratorio ATA API",
    description="Base backend FastAPI + MongoDB for Laboratorio ATA",
    version="0.1.0"
)

# Registra el manejador de rate limit
register_rate_limit_handler(app)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(technicians.router)
app.include_router(users.router)

@app.get("/")
@limiter.limit("10/minute")  
async def root():
    return {"message": "API is running 🚀"}