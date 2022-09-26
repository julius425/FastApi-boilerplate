import os
import pathlib

import aioredis
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi_pagination import add_pagination
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

import app.admin
from app.core.config import settings
from app.core.exception import add_exception_handlers
from app.models.users import Admin
from app.v1.api import router as v1_router


def create_app():
    app = FastAPI(middleware=[
        Middleware(
            CORSMiddleware, allow_origins=['*'], allow_credentials=True,
            allow_methods=['*'], allow_headers=['*']
        )
    ])

    static_dir = os.path.join(settings.ROOT_DIR, "app", "static")
    pathlib.Path(static_dir).mkdir(parents=True, exist_ok=True)  # create if not exists
    app.mount(
        '/static',
        StaticFiles(directory=static_dir),
        name='static',
    )

    app.include_router(v1_router, prefix='/v1')
    add_exception_handlers(app)

    @app.on_event("startup")
    async def startup():
        redis = aioredis.from_url(
            "redis://redis/0",
            decode_responses=True,
            encoding="utf8",
        )
        await admin_app.configure(
            logo_url="https://preview.tabler.io/static/logo-white.svg",
            template_folders=[os.path.join(settings.ROOT_DIR, "app", "templates")],
            providers=[
                UsernamePasswordProvider(
                    admin_model=Admin,
                    login_logo_url="https://preview.tabler.io/static/logo.svg",
                )
            ],
            redis=redis,
        )

    app.mount("/admin", admin_app)
    register_tortoise(
        app=app,
        db_url=settings.DATABASE_URL,
        modules={'models': settings.TORTOISE_MODELS},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    add_pagination(app)

    return app


TORTOISE_ORM = {
        "connections": {"default": settings.DATABASE_URL},
        "apps": {
            "models": {
                "models": [
                    "app.models.codes", "app.models.users",
                    "aerich.models"
                ],
                "default_connection": "default",
            },
        },
    }



app = create_app()
