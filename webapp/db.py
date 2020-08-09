""" Database helper module to make interactions with psycopg2 easier. """
import logging
import psycopg2
import pandas as pd
from webapp import config


LOGGER = logging.getLogger(__name__)


def get_dataframe(sql_raw, params=None):
    """Executes `sql_raw` and returns results as `Pandas.DataFrame`.

    Parameters
    ----------------
    sql_raw : str
        SQL query to execute.

    params : dict
        (Optional) Parameters to pass into query.

    Returns
    ----------------
    results : pandas.DataFrame
        Returns False if DB error.
    """
    try:
        conn = get_db_conn()
    except psycopg2.ProgrammingError as err:
        LOGGER.error('Connection (%s) not configured properly.  Err: %s',
                     connection_name,
                     err)
        return False

    if not conn:
        return False

    results = pd.read_sql(sql_raw, conn, params=params)
    return results


def get_db_conn():
    """Establishes psycopg2 database connection."""
    db_string = config.DATABASE_STRING

    try:
        conn = psycopg2.connect(db_string)
        config.DB_CONN_AVAILABLE = True
    except psycopg2.OperationalError as err:
        config.DB_CONN_AVAILABLE = False
        err_msg = 'Database connection error.  Error: {}'.format(err)
        LOGGER.error(err_msg)
        return False
    return conn

