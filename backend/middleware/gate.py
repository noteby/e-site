import http
import time
#
from loguru import logger
from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Scope, Receive, Send


class GateMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != 'http':  # http | websocket | lifespan
            return await self.app(scope, receive, send)
        #
        start_ts = time.time()
        status: int = 0
        err_body: dict | None = None

        async def send_wrapper(message: Message) -> None:
            nonlocal status, err_body
            if message['type'] == 'http.response.start':
                status = message['status']

            elif message['type'] == 'http.response.body':
                if status >= http.HTTPStatus.BAD_REQUEST:
                    err_body = message['body'].decode()
            #
            await send(message)

        await self.app(scope, receive, send_wrapper)
        #
        headers = {k: v for k, v in MutableHeaders(scope=scope).items()
                   if k in [
                       'host',
                       'content-type',
                       'content-length',
                       'user-agent',
                   ]}

        request = {
            'method': scope['method'],
            'path': scope['path'],
            'status': status,
            'err_body': err_body,
            'client': ':'.join([str(i) for i in scope['client']]),
            'headers': headers,
        }
        logger.info(f'Duration:{time.time() - start_ts:.6f}s, request:{request}')
