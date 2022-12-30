from fastapi import APIRouter
#
from .v1.auth import router as v1_auth
from .v1.user import router as v1_user
from .v1.note import router as v1_note, \
    own_router as v1_own_note

# v1
v1 = APIRouter(prefix='/v1')
v1.include_router(v1_auth, prefix='/auth')
v1.include_router(v1_user, prefix='/user')
v1.include_router(v1_note, prefix='/note')

# v1 - own
v1.include_router(v1_own_note, prefix='/own/note')
