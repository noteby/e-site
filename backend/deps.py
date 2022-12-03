from fastapi import Request
from sqlalchemy.orm import Session
#
from .database.engine import SessionLocal
from .utils.request import RequestInfo


def get_db() -> Session:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def filter_request_payload(request: Request):
    request_info: RequestInfo = request.scope['request_info']
    await request_info.filter_payload(request)
