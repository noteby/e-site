from fastapi import Form
# from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, EmailStr


class SimpleOAuth2PasswordRequestForm:
    def __init__(
            self,
            email: EmailStr = Form(),
            password: str = Form(),
            scope: str = Form(default='default'),
            grant_type: str = Form(default=None, regex='password'),

    ):
        self.email = email
        self.password = password
        self.scopes = scope.split()
        # self.grant_type = grant_type


class NoteBaseInfoReq(BaseModel):
    title: str = Field(max_length=36)
    content: str


class CreateNoteReq(NoteBaseInfoReq):
    display: bool | None = Field(default=False)


class UpdateNoteReq(CreateNoteReq):
    ...
