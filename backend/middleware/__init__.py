from fastapi.middleware import Middleware
#
from .gate import GateMiddleware

# https://www.starlette.io/middleware/#pure-asgi-middleware
middleware = [
    Middleware(GateMiddleware),
]
