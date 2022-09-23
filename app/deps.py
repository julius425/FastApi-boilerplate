from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from app.services.users import UserService


async def get_current_user(authorize: AuthJWT = Depends(), users: UserService = Depends()):
    authorize.jwt_required()
    return await users.get_by_email(authorize.get_jwt_subject())
