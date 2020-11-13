import os
import logging
import json
from flask import session
from packaging.version import parse as parse_version
from pgdd_ui import config, db


LOGGER = logging.getLogger(__name__)


def save_json(data, out_name):
    out_dir = config.BUILD_PATH
    data_out = json.dumps(data)
    out_file = os.path.join(out_dir, out_name)
    with open(out_file, "w") as f:
        f.write(data_out)


def version():
    """Returns the PgDD version installed in the connected database.

    Returns
    ------------------
    version : packaging.version.Version
        PgDD extension currently uses `version.major` and `version.minor`.
        Complies to PEP 440 versioning.
    """
    if config.CHECK_PGDD_VERSION:
        sql_raw = "SELECT extversion FROM pg_catalog.pg_extension "
        sql_raw += " WHERE extname = 'pgdd' LIMIT 1;"
        results = db.get_data(sql_raw, params=None,
                              single_row=True)
        version = parse_version(results['extversion'])
    else:
        version = min_supported_version()
        msg = 'PgDD version check disabled. Defaulting to min supported %s'
        LOGGER.warn(msg, version)
    return version

def min_supported_version():
    """Returns minimum supported version of PgDD for UI to function.

    Returns
    ------------------
    version : packaging.version.Version
    """
    min_version = '0.3'
    version = parse_version(min_version)
    return version



def get_table_tree():
    """Runs multiple queries to collect data for tree display.

    Returns
    ---------------------
    data : dict
        Keys: schemas, tables, columns
    """
    schemas = get_object_list('schemas', return_format='RealDict')
    print(f'Type: schemas {type(schemas)}')
    tables = get_object_list('tables', return_format='RealDict')
    columns = get_object_list('columns', return_format='RealDict')
    data = {'schemas': schemas,
            'tables': tables,
            'columns': columns}
    return data

def schemas():
    """Queries database for schema level details.
    """
    sql_raw = """SELECT s_name, description, table_count,
                view_count, function_count,
                size_pretty, size_plus_indexes,
                size_bytes::FLOAT AS size_bytes, data_source, sensitive
            FROM dd_ui.get_schemas()
"""
    sql_raw += ' WHERE NOT system_object '
    sql_raw += ' ORDER BY s_name'
    params = None
    data = db.get_data(sql_raw, params)
    save_json(data, 'schemas.json')


def tables():
    """Queries database for table details.
    """
    sql_raw = 'SELECT * FROM dd_ui.get_tables() '
    sql_raw += ' WHERE NOT system_object '
    sql_raw += ' ORDER BY s_name, t_name'
    params = None
    data = db.get_data(sql_raw, params)
    save_json(data, 'tables.json')

def views():
    """Queries database for view details.
    """
    sql_raw = 'SELECT * FROM dd_ui.get_views() '
    sql_raw += ' WHERE NOT system_object '
    sql_raw += ' ORDER BY s_name, v_name'
    params = None
    data = db.get_data(sql_raw, params)
    save_json(data, 'views.json')


def columns():
    """Queries database for column details for views and tables.
    """
    sql_raw = 'SELECT * FROM dd_ui.get_columns() '
    sql_raw += ' WHERE NOT system_object '
    sql_raw += ' ORDER BY s_name, t_name, position'
    params = None
    data = db.get_data(sql_raw, params)
    save_json(data, 'columns.json')

def functions():
    """Queries database for function details.
    """
    sql_raw = 'SELECT * FROM dd_ui.get_functions() '
    sql_raw += ' WHERE NOT system_object '
    sql_raw += ' ORDER BY s_name, f_name'
    params = None
    data = db.get_data(sql_raw, params)
    save_json(data, 'functions.json')



class DatabaseStats():
    """Object representing database-level details."""
    def __init__(self):
        """Load details to attributes to avoid requerying too frequently.
        """
        self.pgdd_version = version()
        self.pg_version_full = self.pg_version_full()
        self.pg_version_short = self.pg_version_short()
        self.pg_host = config.DB_HOST
        self.pg_port = config.DB_PORT
        self.pg_db = config.DB_NAME

    def pg_version_full(self):
        """Returns PostgreSQL version from `SELECT version()`

        Example:
            PostgreSQL 12.4 (Ubuntu 12.4-1.pgdg18.04+1) on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0, 64-bit

        Returns
        ------------------
        version : str
        """
        sql_raw = "SELECT version();"
        results = db.get_data(sql_raw, params=None,
                              single_row=True)
        pg_version = results['version']
        return pg_version

    def pg_version_short(self):
        """Returns shorter PostgreSQL version from `SHOW server_version;`

        Example:
            12.4 (Ubuntu 12.4-1.pgdg18.04+1)

        Returns
        ------------------
        version : str
        """
        sql_raw = "SHOW server_version;"
        results = db.get_data(sql_raw, params=None,
                              single_row=True)
        pg_version = results['server_version']
        return pg_version
