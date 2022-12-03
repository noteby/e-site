import http
#
from starlette.types import ASGIApp, Message, Scope, Receive, Send
#
from backend.utils.request import RequestInfo


class GateMiddleware:
    """
    - generate trace info
    - logged request info
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != 'http':  # http | websocket | lifespan
            return await self.app(scope, receive, send)
        # Request info
        request_info = RequestInfo()
        request_info.filter_base(scope)
        scope['request_info'] = request_info

        async def send_wrapper(message: Message) -> None:
            nonlocal request_info
            if message['type'] == 'http.response.start':
                request_info.status = message['status']

            elif message['type'] == 'http.response.body':
                # If status >= 400, will logged body
                if request_info.status >= http.HTTPStatus.BAD_REQUEST:
                    request_info.level = 'WARNING'
                    request_info.err_resp = message['body'].decode()
            #
            await send(message)

        await self.app(scope, receive, send_wrapper)

        request_info.log()
