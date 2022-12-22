from fastapi import APIRouter, Depends
#
from backend.definer.response import UserInfo
from backend.deps import current_user
from backend.internal.user import User

router = APIRouter(tags=['User'])


@router.get('/info', response_model=UserInfo)
def user_info(user: User = Depends(current_user)):
    return UserInfo(email=user.email)
