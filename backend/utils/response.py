import time
from typing import Any
#
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class ErrorResp(BaseModel):
    code: int
    desc: str
    detail: Any
    timestamp: int = Field(default_factory=lambda: int(time.time()))


def make_response(
        code: int, desc: str, detail: Any = None,
        status_code: int = 200, headers: dict[str, str] | None = None
):
    return JSONResponse(
        content=ErrorResp(
            code=code,
            desc=desc,
            detail=detail,
        ).dict(),
        status_code=status_code,
        headers=headers
    )
