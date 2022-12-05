import secrets
# 
from fastapi import Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
#
from .database.engine import SessionLocal
from .utils.request import RequestInfo
from backend.utils.errors.errorcode import HttpError
from backend.utils.errors.exceptions import ApiException


async def get_db() -> Session:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def filter_request_payload(request: Request):
    request_info: RequestInfo = request.scope['request_info']
    await request_info.filter_payload(request)


security = HTTPBasic()


def basic_auth(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    def _compare_digest(_current: str, _correct: str):
        return secrets.compare_digest(
            _current.encode('utf8'),
            _correct.encode('utf8'),
        )

    is_correct_username = _compare_digest(credentials.username, 'admin')
    is_correct_password = _compare_digest(credentials.password, 'admin')
    if not (is_correct_username and is_correct_password):
        raise ApiException(
            HttpError.unauthorized,
            detail='Incorrect username or password',
            headers={'www-authenticate': 'Basic'},
        )

    return credentials.username
