from pydantic import BaseModel
#
from . import schema


class LoginRes(BaseModel):
    token: str
    user: schema.UserBaseInfo
