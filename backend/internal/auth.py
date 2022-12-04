from datetime import datetime, timedelta
#
from jose import JWTError, jwt

SECRET_KEY = '0x123'
ALGORITHM = 'HS256'
DEFAULT_EXPIRE_MINUTES = 60 * 24 * 3


def create_access_token(data: dict, expires_minutes: int|None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=expires_minutes or DEFAULT_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
