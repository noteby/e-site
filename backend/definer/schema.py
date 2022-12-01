from datetime import datetime
#
from pydantic import BaseModel
from pydantic import EmailStr


class UserBaseInfo(BaseModel):
    id: int
    email: EmailStr
    last_login: datetime
