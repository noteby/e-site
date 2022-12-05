from typing import Optional, Any, Mapping
#
from .errorcode import ErrorCode


class _BaseException(Exception):
    pass


class SetupException(_BaseException):
    pass


class ApiException(_BaseException):
    def __init__(
            self, e: ErrorCode, detail: Any = None,
            headers: Optional[Mapping[str, str]] = None,
    ):
        self.code = e.code
        self.desc = e.desc
        self.detail = detail if detail else e.detail

        self.headers = headers
        self.status_code = e.status_code
