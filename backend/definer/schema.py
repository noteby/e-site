from datetime import datetime
from typing import List
#
from pydantic import BaseModel, Field
from pydantic import EmailStr


class JwtData(BaseModel):
    sub: str
    exp: datetime = Field(
        default_factory=lambda: datetime.utcnow()
    )
    #
    uid: int
    scopes: List[str]


class UserBaseInfo(BaseModel):
    id: int
    email: EmailStr
    last_login: datetime
