from typing import Any, Dict
from loguru import logger
from pydantic import BaseModel, ValidationError
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#
from backend.settings import database_config
from backend.utils.exceptions import SetupException


class Config(BaseModel):
    url: str
    echo: bool = False
    connect_args: Dict[Any, Any] = {}


try:
    config = Config(**database_config)
except ValidationError as e:
    logger.error(f'Database config error, {e.json()}')
    raise SetupException

engine: Engine = create_engine(**config.dict())
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def setup():  # Mock

    logger.debug('Database setup ok')
