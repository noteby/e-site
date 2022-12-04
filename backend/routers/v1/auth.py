from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
#
from backend.definer.request import LoginForm
from backend.definer.response import Token
from backend.deps import get_db
from backend.internal.auth import create_access_token
from backend.internal.user import authenticate_user
from backend.utils.errors.errorcode import HttpError
from backend.utils.errors.exceptions import ApiException

auth = APIRouter(tags=['Auth'])


@auth.post('/token', response_model=Token)
def get_access_token(req: LoginForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, email=req.email, password=req.password)
    if not user:
        raise ApiException(HttpError.unauthorized, detail='Invalid email or password')

    access_token = create_access_token(
        data={'sub': user.email},
    )
    return Token(access_token=access_token)
