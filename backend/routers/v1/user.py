from fastapi import APIRouter, Depends
#
from backend.definer.response import UserInfoRes
from backend.deps import current_user
from backend.internal.user import User

router = APIRouter(tags=['User'])


@router.get('/info', response_model=UserInfoRes)
def user_info(user: User = Depends(current_user)):
    return UserInfoRes(email=user.email)
