from pydantic import BaseModel, validator
from pydantic.networks import EmailStr
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.users import User


User_Pydantic = pydantic_model_creator(User, name='User', exclude=('password',))
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude=('id', 'status'))
UpdateUser_Pydantic = pydantic_model_creator(User, name='UserUpdate',
                                             exclude=('id', 'status', 'email', 'password'))


class UserEmailAuth(BaseModel):
    email: EmailStr
    password: str


