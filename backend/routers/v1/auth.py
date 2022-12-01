from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
#
from backend.definer.request import LoginForm
from backend.definer.response import LoginRes
from backend.definer.schema import UserBaseInfo
from backend.deps import get_db
from backend.internal.user import get_user_by_email

auth = APIRouter(tags=['Auth'])


@auth.post('/login', response_model=LoginRes)
def login(req: LoginForm = Depends(), db: Session = Depends(get_db)):
    # Test
    user = get_user_by_email(db, email=req.email)
    print('>>>', user)

    return LoginRes(token='x', user=UserBaseInfo(
        id=1,
        email='x@mail.com',
        last_login='2022-12-01 00:00:00.000'
    ))


@auth.post('/logout')
def logout():
    return 'logout'
