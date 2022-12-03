from fastapi import FastAPI, Depends
#
from .deps import filter_request_payload
from .middleware import middleware
from .routers import router
from .setup import setup

api = FastAPI(
    version='0.1.0',
    middleware=middleware,
    dependencies=[Depends(filter_request_payload)],
)


@api.on_event("startup")
async def startup_event():
    # Setup
    if not setup():
        raise RuntimeError('Setup error')
    # Router
    api.include_router(router.v1)
