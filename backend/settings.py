from pathlib import Path
#
from pydantic import BaseModel, BaseSettings
from pydantic.config import Extra as __Extra

backend_dir: Path = Path(__file__).parent


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

    auth: _Auth
    database: _Database


def load_settings() -> Settings:
    import tomllib
    with open(
            backend_dir / '.toml', 'rb'
    ) as f:
        data = tomllib.load(f)
    return Settings(**data)


settings = load_settings()

# from pprint import pprint
# print(settings.dict())
