import secrets
from typing import Optional
# 
from fastapi import Depends, Request, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials, SecurityScopes
from sqlalchemy.orm import Session
#
from .database.engine import SessionLocal
from .database.models import User
from .internal import auth
from .utils.errors.errorcode import HttpError
from .utils.errors.exceptions import ApiException
from .utils.request import RequestInfo

http_basic = HTTPBasic()


async def get_db() -> Session:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def filter_request_payload(request: Request):
    request_info: RequestInfo = request.scope['request_info']
    await request_info.filter_payload(request)


def basic_auth(credentials: HTTPBasicCredentials = Depends(http_basic)) -> str:
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


async def current_user(
        security_scopes: SecurityScopes,
        db: SessionLocal = Depends(get_db),
        token: str = Depends(auth.oauth2_scheme),
):
    return await auth.get_current_user(
        db=db,
        security_scopes=security_scopes,
        token=token,
    )


def current_scopes_user(scopes: Optional[list[str]] = None):
    async def inner(
            user: User = Security(current_user, scopes=scopes or ['_null_scope'])
    ):
        return await auth.get_current_scopes_user(user)

    return inner
