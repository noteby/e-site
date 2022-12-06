from fastapi import FastAPI, Depends
#
from .deps import filter_request_payload
from .middleware import middleware
from .openapi import reset_api_doc
from .routers import router
from .setup import setup
from .utils.errors.handlers import exception_handlers
from .utils.response import examples_for_error_response

api = FastAPI(
    debug=False,
    version='0.1.0',
    title='E-Api',
    openapi_url=None,
    middleware=middleware,
    dependencies=[Depends(filter_request_payload)],
    exception_handlers=exception_handlers,
    responses=examples_for_error_response(),
)


@api.on_event("startup")
async def startup_event():
    # Setup
    if not setup():
        raise RuntimeError('Setup error')
    # Doc
    reset_api_doc(api)
    # Router
    api.include_router(router.v1)
