import http
from dataclasses import dataclass
from typing import Any


@dataclass
class ErrorCode:
    code: int
    desc: str
    detail: Any = None
    #
    status_code: int = 200


def parse_http_status(status: Any):
    value: int = int(status.value)
    desc: str = str(status.phrase)
    return ErrorCode(code=value, desc=desc, status_code=value)


class HttpError:
    # 500_
    internal_server_error = parse_http_status(http.HTTPStatus.INTERNAL_SERVER_ERROR)  # 500
    # 400_
    bad_request = parse_http_status(http.HTTPStatus.BAD_REQUEST)  # 400
    unauthorized = parse_http_status(http.HTTPStatus.UNAUTHORIZED)  # 401
    forbidden = parse_http_status(http.HTTPStatus.FORBIDDEN)  # 403
    not_found = parse_http_status(http.HTTPStatus.NOT_FOUND)  # 404
    method_not_allowed = parse_http_status(http.HTTPStatus.METHOD_NOT_ALLOWED)  # 405
    request_timeout = parse_http_status(http.HTTPStatus.REQUEST_TIMEOUT)  # 408
    unprocessable_entity = parse_http_status(http.HTTPStatus.UNPROCESSABLE_ENTITY)  # 422
    too_many_requests = parse_http_status(http.HTTPStatus.TOO_MANY_REQUESTS)  # 429


class ApiError:
    api_error = ErrorCode(code=1000, desc='api error')
