""" Database helper module to make interactions with psycopg2 easier. """
import logging
import psycopg2
import psycopg2.extras
from pgdd_ui import config


LOGGER = logging.getLogger(__name__)


def get_data(sql_raw, params=None, single_row=False):
    """Main query point for all read queries.
    """
    if single_row:
        return _select_one(sql_raw, params)
    else:
        return _select_multi(sql_raw, params)


def _select_one(sql_raw, params):
    """ Runs SELECT query that will return zero or 1 rows.
    `params` is required but can be set to None if a LIMIT 1 is used.

    Parameters
    --------------------
    sql_raw : str
        Query string to execute.

    params : dict
        Parameters to pass into `sql_raw`

    Returns
    --------------------
    results
    """
    results = _execute_query(sql_raw, params, 'sel_single')
    return results


def _select_multi(sql_raw, params=None):
    """ Runs SELECT query that will return multiple (all) rows.

    Parameters
    --------------------
    sql_raw : str
        Query string to execute.

    params : dict
        (Optional) Parameters to pass into `sql_raw`

    Returns
    --------------------
    results
    """
    results = _execute_query(sql_raw, params, 'sel_multi')
    return results



def get_db_conn():
    """Establishes psycopg2 database connection."""
    db_string = config.DATABASE_STRING
    conn = psycopg2.connect(db_string)
    return conn


def _execute_query(sql_raw, params, qry_type):
    """ Handles executing queries based on the `qry_type` passed in.

    Returns False if there are errors during connection or execution.

        if results == False:
            print('Database error')
        else:
            print(results)

    You cannot use `if not results:` b/c 0 results is a false negative.

    Parameters
    ---------------------
    sql_raw : str
        Query string to execute.

    params : dict
        (Optional) Parameters to pass into `sql_raw`

    qry_type : str
        Defines how the query is executed. e.g. `sel_multi`
        uses `.fetchall()` while `sel_single` uses `.fetchone()`.
    """
    try:
        conn = get_db_conn()
    except psycopg2.ProgrammingError as err:
        err_msg = 'Connection not configured properly.  Err: %s'
        LOGGER.error(err_msg, err)
        return False

    if not conn:
        return False

    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cur.execute(sql_raw, params)
        if qry_type == 'sel_multi':
            results = cur.fetchall()
        elif qry_type == 'sel_single':
            results = cur.fetchone()
        else:
            raise Exception('Invalid query type defined.')

    except psycopg2.ProgrammingError as err:
        LOGGER.error('Database error via psycopg2.  %s', err)
        results = False
    except psycopg2.IntegrityError as err:
        LOGGER.error('PostgreSQL integrity error via psycopg2.  %s', err)
        results = False
    finally:
        conn.close()

    return results
