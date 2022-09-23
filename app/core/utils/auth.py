from typing import Union
from fastapi_jwt_auth import AuthJWT


def generate_tokens(jwt: AuthJWT, subject: Union[int, str]) -> dict:
    access = jwt.create_access_token(subject=subject)
    refresh = jwt.create_refresh_token(subject=subject)
    return {'access': access, 'refresh': refresh}

