from pathlib import Path

# Dir
backend_dir: Path = Path(__file__).parent
store_dir: Path = backend_dir / 'store'

# Database config
database_config: dict = {
    # https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls
    'url': f"sqlite:///{store_dir / 'dev.db'}",  # sqlite3
    'echo': True,
    'connect_args': {
        'check_same_thread': False
    }
}
