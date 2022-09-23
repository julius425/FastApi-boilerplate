from fastapi import Depends, HTTPException, APIRouter
from fastapi_jwt_auth import AuthJWT

from app.core.utils.auth import generate_tokens
from app.services.users import UserService
from app.schemas.token import AccessTokenResponse, AuthResponse, TokensResponse
from app.schemas.user import UserEmailAuth


router = APIRouter()


@router.post('', response_model=AuthResponse)
async def login_by_email(
    user: UserEmailAuth,
    authorize: AuthJWT = Depends(),
    users: UserService = Depends()
):
    user = await users.authenticate(email=user.email, password=user.password)
    if not user:
        raise HTTPException(400, 'Invalid email/password')

    return AuthResponse(
        tokens=TokensResponse(**generate_tokens(authorize, user.email)),
        user=user
    )


@router.post('/refresh', response_model=AccessTokenResponse)
async def refresh_token(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()

    user_email = authorize.get_jwt_subject()
    access_token = authorize.create_access_token(subject=user_email)
    return AccessTokenResponse(access=access_token)
