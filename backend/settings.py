from pathlib import Path
#
from pydantic import BaseModel, BaseSettings
from pydantic.config import Extra

backend_dir: Path = Path(__file__).parent


class _ApiDoc(BaseModel):
    username: str
    password: str


class _Auth(BaseModel):
    # $ openssl rand -hex 32
    secret_key: str


class _Database(BaseModel):
    # https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls
    url: str
    echo: bool
    connect_args: dict


class Settings(BaseSettings):
    class Config:
        extra: Extra = Extra.allow

    store_dir: Path = backend_dir / 'store'

    api_doc: _ApiDoc
    auth: _Auth
    database: _Database


def load_settings() -> Settings:
    import tomllib
    #
    from loguru import logger
    from pydantic import ValidationError

    def _exit():
        import sys
        logger.error('Load settings failed. Abort process!')
        sys.exit(1)

    file = backend_dir / '.toml'
    if not file.is_file():
        logger.error(f'Toml file not exists, {file}')
        _exit()

    try:
        with open(file, 'rb') as f:
            data = tomllib.load(f)
        return Settings(**data)
    except tomllib.TOMLDecodeError as e:
        logger.error(f'Toml file decode error. {e}')
    except ValidationError as e:
        logger.error(f'Data validation error. {e.json()}')
    except:
        logger.exception('Unknown error')

    _exit()


settings = load_settings()
# from pprint import pprint
# print(settings.dict())
