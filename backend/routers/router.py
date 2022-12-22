from fastapi import APIRouter
#
from .v1.auth import router as auth_v1
from .v1.user import router as user_v1

# v1
v1 = APIRouter(prefix='/v1')
v1.include_router(auth_v1, prefix='/auth')
v1.include_router(user_v1, prefix='/user')
