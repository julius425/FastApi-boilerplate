from fastapi import APIRouter

from app.v1.endpoints import auth, users


# If you use a router for including from fastapi_crudrouter
# you shouldn't define prefix and tags here
router = APIRouter()
router.include_router(auth.router, prefix='/auth', tags=['Auth'])
router.include_router(users.router)
