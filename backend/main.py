from fastapi import FastAPI
#
from .routers import router
from .setup import setup

api = FastAPI(
    version='0.1.0',
)


@api.on_event("startup")
async def startup_event():
    # Setup
    if not setup():
        raise RuntimeError('Setup error')
    # Router
    api.include_router(router.v1)
