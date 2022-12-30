from datetime import datetime
from typing import List
#
from pydantic import BaseModel, Field


class AuthToken(BaseModel):
    access_token: str
    token_type: str = 'Bearer'


class UserInfo(BaseModel):
    email: str


class ListBaseInfoRes(BaseModel):
    count: int


class NoteIDRes(BaseModel):
    note_id: int


class NoteBaseInfoRes(NoteIDRes):
    created_at: datetime = Field(description='2015-05-01T11:00:00')
    title: str


class NoteInfoRes(NoteBaseInfoRes):
    content: str


class NoteListRes(ListBaseInfoRes):
    list: List[NoteBaseInfoRes]


class OwnNoteBaseInfoRes(NoteBaseInfoRes):
    display: bool
    updated_at: datetime | None = Field(description='2015-05-01T11:00:01')


class OwnNoteInfoRes(OwnNoteBaseInfoRes):
    content: str


class OwnNoteListRes(ListBaseInfoRes):
    list: List[OwnNoteBaseInfoRes]
