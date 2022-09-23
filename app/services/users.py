from fastapi import HTTPException

from app.core.security import hash_password, verify_password
from app.schemas.user import User_Pydantic, UserIn_Pydantic, UpdateUser_Pydantic
from app.models.users import User


class UserService:
    async def create(self, user: UserIn_Pydantic) -> User_Pydantic:
        user_obj = await User.create(
            **user.dict(exclude={'password'}),
            password=hash_password(user.password)
        )
        return await User_Pydantic.from_tortoise_orm(user_obj)

    async def exists_by_email(self, email: str) -> bool:
        return await User.filter(email=email).exists()

    async def get_by_email(self, email: str) -> User_Pydantic:
        user = await User.get_or_none(email=email)
        return await User_Pydantic.from_tortoise_orm(user)

    async def authenticate(self, email: str, password: str) -> User_Pydantic:
        user = await User.get_or_none(email=email)
        if user and verify_password(password, user.password):
            return await User_Pydantic.from_tortoise_orm(user)

    async def update(self, user_id: int, user: UpdateUser_Pydantic) -> User_Pydantic:
        if user.company_name and not user.INN:
            raise HTTPException(400, 'Вы не обладаете статусом компании')

        await User.filter(id=user_id).update(
            **user.dict(exclude_unset=True)
        )

        updated_user = await User.get(id=user_id)
        if updated_user.INN and updated_user.status == User.STATUSES[0]:
            # Set company status
            updated_user.status = User.STATUSES[1]
            await updated_user.save(update_fields=('status',))

        return await User_Pydantic.from_tortoise_orm(updated_user)

    async def reset_password(self, user_id: int, password: str):
        await User.filter(id=user_id).update(password=hash_password(password))
        return True

    async def reset_contact_fields(self, user_id: int, **kwargs):
        for field in kwargs.keys():
            assert field in User.get_contact_fields(), 'The field is not a contact'
        return await User.filter(id=user_id).update(**kwargs)
