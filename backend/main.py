from fastapi import FastAPI, Depends
#
from .deps import filter_request_payload
from .middleware import middleware
from .routers import router
from .setup import setup
from .utils.errors.handlers import exception_handlers

api = FastAPI(
    debug=False,
    version='0.1.0',
    middleware=middleware,
    dependencies=[Depends(filter_request_payload)],
    exception_handlers=exception_handlers,
)


@api.on_event("startup")
async def startup_event():
    # Setup
    if not setup():
        raise RuntimeError('Setup error')
    # Router
    api.include_router(router.v1)
