from typing import Any
#
from .errorcode import ErrorCode


class _BaseException(Exception):
    pass


class SetupException(_BaseException):
    pass


class ApiException(_BaseException):
    def __init__(self, e: ErrorCode, detail: Any = None):
        self.code: int = e.code
        self.desc: str = e.desc
        self.detail: Any = detail if detail else e.detail

        self.status_code: int = e.status_code
