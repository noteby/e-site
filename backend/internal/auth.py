from datetime import datetime, timedelta
from typing import List
#
from fastapi import Depends, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr, ValidationError
#
from backend.database.engine import SessionLocal
from backend.internal.user import User, get_user_by_email
from backend.utils.errors.errorcode import HttpError
from backend.utils.errors.exceptions import ApiException

SECRET_KEY = '0x123'
ALGORITHM = 'HS256'
DEFAULT_EXPIRE_MINUTES = 60 * 24 * 3

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/v1/auth/token',
    scopes={
        'default': 'Default',
        'dev': 'Use by developer',
    },
)


class TokenData(BaseModel):
    email: EmailStr = None
    scopes: List[str] = []


def create_access_token(
        data: dict, expires_minutes: int | None = None,
):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=expires_minutes or DEFAULT_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
        db: SessionLocal,
        security_scopes: SecurityScopes,
        token: str = Depends(oauth2_scheme)
):
    #
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = 'Bearer'
    # Credentials exception
    exc = ApiException(
        HttpError.unauthorized,
        detail='Could not validate credentials',
        headers={'www-authenticate': authenticate_value},
    )
    try:
        # Decode jwt
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        scopes: List = payload.get('scopes', [])
        # Validate
        token_data = TokenData(scopes=scopes, email=email)
    except (JWTError, ValidationError):
        raise exc
    # Get user
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise exc
    # Scope
    for scope in security_scopes.scopes:
        if scope in token_data.scopes:
            continue
        exc.detail = 'Not enough permissions'
        raise exc

    if user.disabled:
        raise ApiException(
            HttpError.bad_request,
            detail='Inactive user'
        )

    return user


async def get_current_scopes_user(
        user: User = Security(get_current_user, scopes=['default'])
):
    return user
