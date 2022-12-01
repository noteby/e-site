from fastapi import APIRouter
#
from .v1.auth import auth as auth_v1

# v1
v1 = APIRouter(prefix='/v1')
v1.include_router(auth_v1, prefix='/auth')
