""" PgDD-UI site generator __init__.py file """
import logging
from pgdd_ui import config, pgdd


# Setup Logging
LOG_PATH = config.LOG_PATH
LOGGER = logging.getLogger(__name__)
HANDLER = logging.FileHandler(filename=LOG_PATH, mode='a+')
FORMATTER = logging.Formatter(config.LOG_FORMAT)
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)

if config.APP_DEBUG:
    LOGGER.setLevel(logging.DEBUG)
else:
    LOGGER.setLevel(logging.INFO)

LOGGER.info('PgDD UI builder initialized')
pgdd_version = pgdd.version()
LOGGER.info(f'PgDD extension version: {pgdd_version.major}.{pgdd_version.minor}')
