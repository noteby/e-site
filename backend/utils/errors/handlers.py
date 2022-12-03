from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as OriHttpException
#
from .errorcode import HttpError
from .exceptions import ApiException
from backend.utils.response import make_response


async def http_exception_handler(
        request: Request, exc: OriHttpException
):
    return make_response(
        code=exc.status_code,
        desc=exc.detail,
        status_code=exc.status_code,
        headers=exc.headers,
    )


async def request_validation_error_handler(
        request, exc: RequestValidationError
):
    e = HttpError.unprocessable_entity
    return make_response(
        code=e.code,
        desc=e.desc,
        detail=exc.errors(),
        status_code=e.status_code,
    )


async def api_exception_handler(request, exc: ApiException):
    return make_response(**exc.__dict__)


exception_handlers = {
    #
    OriHttpException: http_exception_handler,
    RequestValidationError: request_validation_error_handler,
    #
    ApiException: api_exception_handler,
    #
}
