def _setup():
    from .utils.logger import setup as logger_setup
    logger_setup()

    from .database.engine import setup as db_setup
    db_setup()


def setup():
    from loguru import logger
    #
    from .utils.exceptions import SetupException

    try:
        _setup()
        logger.info('Setup finished')
        return True
    except Exception as e:
        if not isinstance(e, SetupException):
            logger.exception('Unknown setup error')

        return False
