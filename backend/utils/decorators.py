import time
from functools import wraps
#
from loguru import logger


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_at = time.time()
        result = func(*args, **kwargs)
        logger.info(
            f'[Timer] at <{func.__name__}>: {time.time() - start_at:.6f}s'
        )
        return result

    return wrapper
