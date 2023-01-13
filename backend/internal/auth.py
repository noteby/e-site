from datetime import datetime, timedelta
#
from fastapi import Depends, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from pydantic import ValidationError
#
from backend.database.engine import SessionLocal
from backend.definer.schema import JwtData
from backend.internal.user import User, get_user_by_email
from backend.settings import settings
from backend.utils.errors.errorcode import HttpError
from backend.utils.errors.exceptions import ApiException

SECRET_KEY = settings.auth.secret_key
#
ALGORITHM = 'HS256'
#
# DEFAULT_EXPIRE_MINUTES = 60 * 24 * 3
DEFAULT_EXPIRE_MINUTES = settings.auth.expire_minutes

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/v1/auth/token',
    scopes={
        'default': 'Default',
        'dev': 'Use by developer',
    },
)


def create_access_token(
        data: JwtData, expires_minutes: int | None = None,
):
    data.exp = datetime.utcnow() + timedelta(
        minutes=expires_minutes or DEFAULT_EXPIRE_MINUTES
    )
    encoded_jwt = jwt.encode(
        data.dict(), SECRET_KEY, algorithm=ALGORITHM
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
        # Validate
        jwt_data = JwtData(**payload)
    except (JWTError, ValidationError):
        raise exc
    # Get user
    user = get_user_by_email(db, email=jwt_data.sub)
    if user is None or user.id != jwt_data.uid:
        raise exc
    # Check scope
    for scope in security_scopes.scopes:
        if scope in jwt_data.scopes:
            continue
        exc.detail = 'Not enough permissions'
        raise exc

    if user.disabled:
        raise ApiException(
            HttpError.bad_request,
            detail='Inactive user'
        )

    return user


async def get_current_scopes_user(user: User = Security(
    get_current_user, scopes=['default']
)):
    return user
