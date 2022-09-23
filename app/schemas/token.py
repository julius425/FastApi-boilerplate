from pydantic import BaseModel

from app.schemas.user import User_Pydantic


class AccessTokenResponse(BaseModel):
    access: str


class TokensResponse(AccessTokenResponse):
    refresh: str


class AuthResponse(BaseModel):
    tokens: TokensResponse
    user: User_Pydantic
