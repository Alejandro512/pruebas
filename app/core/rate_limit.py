from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

# Instancia global del limitador
limiter = Limiter(key_func=get_remote_address)

# Manejo de error por exceso de peticiones
def register_rate_limit_handler(app: FastAPI):
    @app.exception_handler(429)
    async def rate_limit_handler(request: Request, exc):
        return JSONResponse(
            status_code=HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Rate limit exceeded. Try again later."}
        )

    app.state.limiter = limiter
    app.add_exception_handler(HTTP_429_TOO_MANY_REQUESTS, _rate_limit_exceeded_handler)
