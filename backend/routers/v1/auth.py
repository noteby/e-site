from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
#
from backend.definer.request import SimpleOAuth2PasswordRequestForm
from backend.definer.response import AuthToken
from backend.deps import get_db, current_user, current_scopes_user
from backend.internal.auth import create_access_token
from backend.internal.user import User, authenticate_user
from backend.utils.errors.errorcode import HttpError
from backend.utils.errors.exceptions import ApiException

router = APIRouter(tags=['Auth'])


@router.post('/token', response_model=AuthToken)
def login_for_token(
        req: SimpleOAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, email=req.email, password=req.password)
    if not user:
        raise ApiException(
            HttpError.unauthorized, detail='Invalid email or password',
            headers={'www-authenticate': 'Bearer'}
        )

    access_token = create_access_token(
        data={'sub': user.email, 'scopes': req.scopes},
    )
    return AuthToken(access_token=access_token)


@router.get('/test')
async def test(user: User = Depends(current_user)):
    return user.email


@router.get('/test_default_scope')
async def test_default_scope(user: User = Depends(
    current_scopes_user(scopes=['default'])
)):
    return user.email
