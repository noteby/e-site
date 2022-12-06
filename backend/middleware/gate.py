import http
from uuid import uuid4
#
from loguru import logger
from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Scope, Receive, Send
#
from backend.utils.context import request_id
from backend.utils.errors.errorcode import HttpError
from backend.utils.errors.exceptions import ApiException
from backend.utils.request import RequestInfo
from backend.utils.response import make_response


class GateMiddleware:
    """
    - generate trace info
    - logged request info
    """

    header_request_id: str = 'X-Request-ID'

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != 'http':  # http | websocket | lifespan
            return await self.app(scope, receive, send)
        #
        request_id.set(uuid4().hex)
        #
        request_info = RequestInfo()
        request_info.filter_base(scope)
        scope['_request_info'] = request_info

        async def send_wrapper(message: Message) -> None:
            nonlocal request_info
            if message['type'] == 'http.response.start':
                request_info.status = message['status']
                #
                headers = MutableHeaders(scope=message)
                headers[self.header_request_id] = request_id.get()

            elif message['type'] == 'http.response.body':
                # If status >= 400, will logged body
                if request_info.status >= http.HTTPStatus.BAD_REQUEST:
                    request_info.err_resp = message['body'].decode()
            #
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        except Exception as _:
            e = HttpError.internal_server_error
            logger.exception(e.desc)
            exc = ApiException(e)
            #
            request_info.status = exc.status_code
            response = make_response(**exc.__dict__)
            #
            await response(scope, receive, send)
        finally:
            request_info.log()
