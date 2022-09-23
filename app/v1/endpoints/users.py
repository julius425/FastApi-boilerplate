from fastapi import Depends, HTTPException
from fastapi_crudrouter import TortoiseCRUDRouter
from fastapi_jwt_auth import AuthJWT
from fastapi.background import BackgroundTasks

from app.core.utils.auth import generate_tokens
from app.core.utils.core import send_email, generate_code
from app.deps import get_current_user
from app.models.users import User
from app.schemas.codes import EmailCodeIn_Pydantic
from app.schemas.user import User_Pydantic, UserIn_Pydantic, UpdateUser_Pydantic
from app.schemas.token import AuthResponse, TokensResponse
from app.services.codes import EmailCodeService
from app.services.users import UserService


router = TortoiseCRUDRouter(
    schema=User_Pydantic,
    db_model=User,
    delete_all_route=False,
)


@router.post('', response_model=AuthResponse, status_code=201)
async def create_user(
    user: UserIn_Pydantic,
    users: UserService = Depends(),
    authorize: AuthJWT = Depends(),
):
    print(user.dict())
    if not await users.exists_by_email(email=user.email):
        new_user = await users.create(user)
        return AuthResponse(
            tokens=TokensResponse(**generate_tokens(authorize, user.email)),
            user=new_user
        )
    raise HTTPException(400, 'incorrect email or password')


@router.put('/{item_id}', response_model=User_Pydantic, status_code=200)
async def update_user(
    item_id: int,
    user: UpdateUser_Pydantic,
    users: UserService = Depends(),
    current_user: User_Pydantic = Depends(get_current_user)
):
    if current_user.id != item_id:
        raise HTTPException(403, 'you cant change user data')
    return await users.update(item_id, user)


@router.put('/{item_id}/reset-password', response_model=dict, status_code=200)
async def reset_password(
    item_id: int,
    password: str,
    users: UserService = Depends(),
    current_user: User_Pydantic = Depends(get_current_user)
):
    if current_user.id != item_id:
        raise HTTPException(403, 'you cant change user data')

    try:
        return {'success': await users.reset_password(item_id, password)}
    except:
        return {'success': False}


@router.get('', response_model=User_Pydantic)
async def get_current_user(user: User_Pydantic = Depends(get_current_user)):
    return user

@router.post('/reset-email')
async def send_reset_email_code(
    email: str,
    background_tasks: BackgroundTasks,
    codes: EmailCodeService = Depends(),
    users: UserService = Depends(),
):
    if await users.exists_by_email(email):
        raise HTTPException(400, 'Пользователь с таким email существует')

    code = generate_code()
    await codes.create(EmailCodeIn_Pydantic(email=email, code=code))
    send_email(background_tasks, 'Смена email', email, f'Код подтверждения: {code}')
    return {'success': True}


@router.post('/reset-email/verify')
async def send_reset_email_code_verify(
    code: EmailCodeIn_Pydantic,
    codes: EmailCodeService = Depends(),
    users: UserService = Depends(),
    current_user: User_Pydantic = Depends(get_current_user)
):
    if await codes.verify_code(code):
        await users.reset_contact_fields(current_user.id, email=code.email)
        return {'success': True}
    return {'success': False}
