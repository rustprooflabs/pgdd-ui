import os
import logging

CURR_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_BASE_PATH = os.path.abspath(os.path.join(CURR_PATH, os.pardir))

LOG_FORMAT = '%(levelname)s - %(asctime)s - %(name)s - %(message)s'

LOGGER = logging.getLogger(__name__)

# Set to False to disable version checking.
# Useful for non-exension installs (e.g. PGaaS offerings)
CHECK_PGDD_VERSION = True

try:
    LOG_PATH = os.environ['LOG_PATH']
except KeyError:
    LOG_PATH = PROJECT_BASE_PATH + '/webapp.log'

try:
    APP_DEBUG = os.environ['APP_DEBUG']
except KeyError:
    APP_DEBUG = False


# Required for CSRF protection in Flask, please set to something secret!
try:
    APP_SECRET_KEY = os.environ['APP_SECRET_KEY']
except KeyError:
    ERR_MSG = '\nSECURITY WARNING: To ensure security please set the APP_SECRET_KEY'
    ERR_MSG += ' environment variable.\n'
    LOGGER.warning(ERR_MSG)
    print(ERR_MSG)
    APP_SECRET_KEY = '522ab51267576d482599d314304307c61cb03001d5593db74fce191fb399bf3b'


try:
    DB_HOST, DB_NAME, DB_USER, DB_PW = (os.environ['DB_HOST'],
                                        os.environ['DB_NAME'],
                                        os.environ['DB_USER'],
                                        os.environ['DB_PW'])
    DB_CONN_AVAILABLE = True
except KeyError:
    DB_CONN_AVAILABLE = False
    key_msg = ('Database environment variables not set.'
               'All values are required for proper operation.\n'
               'DB_HOST\nDB_NAME\nDB_USER\nDB_PW\n')
    print(key_msg)
    DB_HOST, DB_NAME, DB_USER, DB_PW = ('127.0.0.1', 'NotSet', 'Invalid', 'Invalid')

if DB_CONN_AVAILABLE:
    try:
        DB_PORT = os.environ['DB_PORT']
    except KeyError:
        DB_PORT = 5432

    MSG = 'DB conn configured. Host: {}; Name: {}; User: {}; Port: {}'
    print(MSG.format(DB_HOST, DB_NAME, DB_USER, DB_PORT))
else:
    DB_PORT = None


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

