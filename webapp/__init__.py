""" PgDD-UI __init__.py file """
import logging
from flask import Flask
from webapp import config, pgdd

# App settings
app = Flask(__name__)
app.config['DEBUG'] = config.APP_DEBUG
app.config['SECRET_KEY'] = config.APP_SECRET_KEY
app.config['WTF_CSRF_ENABLED'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'


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

from webapp import routes

LOGGER.info('PgDD UI initialized')
pgdd_version = pgdd.version()
LOGGER.info(f'PgDD extension version: {pgdd_version.major}.{pgdd_version.minor}')
