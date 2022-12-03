import http
from uuid import uuid4
#
from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Scope, Receive, Send
#
from backend.utils.context import request_id
from backend.utils.request import RequestInfo


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
        scope['request_info'] = request_info

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
                    request_info.level = 'WARNING'
                    request_info.err_resp = message['body'].decode()
            #
            await send(message)

        await self.app(scope, receive, send_wrapper)

        request_info.log()
