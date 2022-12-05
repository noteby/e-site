import time
from typing import Any
#
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorResp(BaseModel):
    code: int
    desc: str
    detail: Any
    timestamp: int


def make_response(
        code: int, desc: str, detail: Any = None,
        status_code: int = 200, headers: dict[str, str] | None = None
):
    return JSONResponse(
        content=ErrorResp(
            code=code,
            desc=desc,
            detail=detail,
            timestamp=int(time.time()),
        ).dict(),
        status_code=status_code,
        headers=headers
    )


def examples_for_error_response():
    from .errors.errorcode import HttpError

    return {e.code: dict(model=ErrorResp, description=e.desc)
            for e in [
                HttpError.bad_request,
                HttpError.unprocessable_entity,
                HttpError.internal_server_error,
            ]}
