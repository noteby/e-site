from pathlib import Path
#
from pydantic import BaseModel, BaseSettings
from pydantic.config import Extra as __Extra

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
    # class Config:
    #     extra: __Extra = __Extra.allow

    store_dir: Path = backend_dir / 'store'

    api_doc: _ApiDoc
    auth: _Auth
    database: _Database


def load_settings() -> Settings:
    import tomllib

    file = backend_dir / '.toml'
    if not file.is_file():
        file.touch()
        print('Toml file not exists, touch it')

    with open(file, 'rb') as f:
        data = tomllib.load(f)

    return Settings(**data)


settings = load_settings()

# from pprint import pprint
# print(settings.dict())
