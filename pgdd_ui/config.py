"""Configuration for PgDD UI.
"""
import os
import logging
from jinja2 import Environment, FileSystemLoader

CURR_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_BASE_PATH = os.path.abspath(os.path.join(CURR_PATH, os.pardir))

LOG_FORMAT = '%(levelname)s - %(asctime)s - %(name)s - %(message)s'

LOGGER = logging.getLogger(__name__)

templates_path = os.path.join(CURR_PATH, 'templates')
J2_ENV = Environment(loader=FileSystemLoader(templates_path),                                                                                                                            
                     trim_blocks=True)

try:
    BUILD_PATH = os.environ['PGDD_BUILD_PATH']
except KeyError:
    BUILD_PATH = os.path.join(PROJECT_BASE_PATH, '_build')

print(f'PgDD building to {BUILD_PATH}')

# Set to False to disable version checking.
# Useful for non-exension installs (e.g. PGaaS offerings)
CHECK_PGDD_VERSION = True

try:
    LOG_PATH = os.environ['LOG_PATH']
except KeyError:
    LOG_PATH = PROJECT_BASE_PATH + '/pgdd-builder.log'

try:
    APP_DEBUG = os.environ['APP_DEBUG']
except KeyError:
    APP_DEBUG = False


try:
    DB_HOST, DB_NAME, DB_USER, DB_PW = (os.environ['DB_HOST'],
                                        os.environ['DB_NAME'],
                                        os.environ['DB_USER'],
                                        os.environ['DB_PW'])
except KeyError:
    key_msg = ('Database environment variables not set.'
               'All values are required for proper operation.\n'
               'DB_HOST\nDB_NAME\nDB_USER\nDB_PW\n')
    print(key_msg)
    DB_HOST, DB_NAME, DB_USER, DB_PW = ('127.0.0.1', 'NotSet', 'Invalid', 'Invalid')


try:
    DB_PORT = os.environ['DB_PORT']
except KeyError:
    DB_PORT = 5432


MSG = 'DB conn configured. Host: {}; Name: {}; User: {}; Port: {}'
print(MSG.format(DB_HOST, DB_NAME, DB_USER, DB_PORT))


def get_db_string():
    """ Builds the database connection string for regular user access.

    Connection string ultimately derived from
    environment vars.

    Returns
    -------------
    database_string : str
    """
    app_name = 'pgdd-ui'
    database_string = 'postgresql://{user}:{pw}@{host}:{port}/{dbname}?application_name={app_name}'

    return database_string.format(user=DB_USER, pw=DB_PW, host=DB_HOST,
                                  port=DB_PORT, dbname=DB_NAME,
                                  app_name=app_name)


DATABASE_STRING = get_db_string()
