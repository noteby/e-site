from pydantic import BaseModel


class AuthToken(BaseModel):
    access_token: str
    token_type: str = 'Bearer'


class UserInfo(BaseModel):
    email: str
