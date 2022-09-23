from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse


def add_exception_handlers(app: FastAPI):
    handlers = {
        AuthJWTException: authjwt_exception_handler
    }

    for exception, handler in handlers.items():
        app.add_exception_handler(exception, handler)


async def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
