import logging
import sys
#
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        # Get corresponding `loguru` level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 6
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(
            depth=depth,
            exception=record.exc_info,
            lazy=True,
        ).log(
            level, record.getMessage()
        )


def setup():
    logger.remove(None)
    #
    logger.add(
        sink=sys.stdout,
        diagnose=False,
        backtrace=False,
        catch=True,
        enqueue=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
               "<level>{level:<8}</level> | "
               "<cyan>{name}</cyan>:"
               "<cyan>{function}</cyan>@"
               "<cyan>{line}</cyan> - "
               "<level>{message}</level>",
    )
    #
    for name in logging.root.manager.loggerDict:
        _logger = logging.getLogger(name)
        if _logger.hasHandlers():
            _logger.propagate = False
            _logger.handlers = [InterceptHandler()]

    logger.debug('Logger setup ok')
