import http
import time
from dataclasses import dataclass, field
from json.decoder import JSONDecodeError
from typing import Any
#
from fastapi import Request
from loguru import logger
from multipart.multipart import parse_options_header
from starlette.datastructures import UploadFile
from starlette.types import Scope


@dataclass
class RequestInfo:
    start_at: float = field(default_factory=time.time)
    #
    duration: str = None  # second
    status: int = 0
    method: str = None
    url: str = None
    headers: list = None
    payload: Any = None
    err_resp: Any = None

    def filter_base(self, scope: Scope):
        request = Request(scope=scope)
        self.method = request.method
        self.url = request.url.__str__()
        #
        _headers = []
        for k, v in request.headers.items():
            if k in ['content-length', 'content-type', 'user-agent']:
                _headers.append((k, v))
        self.headers = _headers

    async def filter_payload(self, request: Request):
        context_type, _ = parse_options_header(
            request.headers.get('content-type')
        )
        # Get payload
        payload: Any
        if context_type == b'application/json':
            try:
                payload = await request.json()
            except JSONDecodeError:
                payload = (await request.body()).decode()
        elif context_type in [
            b'multipart/form-data',
            b'application/x-www-form-urlencoded',
        ]:
            form = await request.form()
            payload: list = form.multi_items()
        else:
            payload = (await request.body()).decode()

        # Get file info
        if payload and context_type == b'multipart/form-data':
            for index, item in enumerate(payload):
                upload_file = item[1]
                if not isinstance(upload_file, UploadFile):
                    continue
                payload[index] = (item[0], dict(
                    name=upload_file.filename,
                    type=upload_file.content_type,
                    size=len(await upload_file.read())  # bytes
                ))
                await upload_file.seek(0)  # https://fastapi.tiangolo.com/zh/tutorial/request-files/#uploadfile_1
        #
        self.payload = payload

    def dict(self):
        return dict(
            duration=f'{time.time() - self.start_at:.6f}',
            status=self.status,
            method=self.method,
            url=self.url,
            headers=self.headers,
            payload=self.payload,
            err_resp=self.err_resp,
        )

    def log(self):
        """
        - logged request info
        """
        if self.status < http.HTTPStatus.BAD_REQUEST:
            __level = 'INFO'
        elif self.status < http.HTTPStatus.INTERNAL_SERVER_ERROR:
            __level = 'WARNING'
        else:
            __level = 'ERROR'

        logger.log(__level, self.dict().__str__())
