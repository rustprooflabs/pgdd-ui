import os
import datetime
import logging
import json
from packaging.version import parse as parse_version
from pgdd_ui import config, db


LOGGER = logging.getLogger(__name__)


def save_json(data, out_name):
    """Serializes data as JSON and saves javascript JSON.parse() to load as var.

    Simply saving the JSON data and attempting to load via local paths will result in error such as:
        Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote resource at file:///path/to/pgdd-ui/_build/db_stats.json. (Reason: CORS request not http).

    A major goal of this project is to provide a simple Data Dictionary output that is easy
    to share regardless of the end user's technical abilities or access to a local Python development
    environment.

    See: https://stackoverflow.com/questions/48362093/cors-request-blocked-in-locally-opened-html
    """
    out_dir = config.BUILD_PATH
    json_data = json.dumps(data)

    js_string = f"var {out_name} = JSON.parse('{json_data}');"
    out_filename = f'{out_name}.js'
    out_file = os.path.join(out_dir, out_filename)
    with open(out_file, "w") as f:
        f.write(js_string)


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


def schemas():
    """Queries database for schema level details.
    """
    sql_raw = 'SELECT * FROM dd_ui.get_schemas() '
    sql_raw += ' WHERE NOT system_object '
    sql_raw += ' ORDER BY s_name'
    params = None
    data = db.get_data(sql_raw, params)
    save_json(data, 'schemas')
    return data


def tables():
    """Queries database for table details.
    """
    sql_raw = 'SELECT * FROM dd_ui.get_tables() '
    sql_raw += ' WHERE NOT system_object '
    sql_raw += ' ORDER BY s_name, t_name'
    params = None
    data = db.get_data(sql_raw, params)
    save_json(data, 'tables')
    return data

def views():
    """Queries database for view details.
    """
    sql_raw = 'SELECT * FROM dd_ui.get_views() '
    sql_raw += ' WHERE NOT system_object '
    sql_raw += ' ORDER BY s_name, v_name'
    params = None
    data = db.get_data(sql_raw, params)
    save_json(data, 'views')
    return data


def columns():
    """Queries database for column details for views and tables.
    """
    sql_raw = 'SELECT * FROM dd_ui.get_columns() '
    sql_raw += ' WHERE NOT system_object '
    sql_raw += ' ORDER BY s_name, t_name, position'
    params = None
    data = db.get_data(sql_raw, params)
    save_json(data, 'columns')
    return data

def functions():
    """Queries database for function details.
    """
    sql_raw = 'SELECT * FROM dd_ui.get_functions() '
    sql_raw += ' WHERE NOT system_object '
    sql_raw += ' ORDER BY s_name, f_name'
    params = None
    data = db.get_data(sql_raw, params)
    save_json(data, 'functions')
    return data


def table_tree():
    """Generates the table tree structure.

    FIXME: Figure out how to build this data better, too much HTML mixed in here.
    """
    schema_data = schemas()
    table_data = tables()
    column_data = columns()

    nested_dd = []
    for s in schema_data:
        #print(s)
        desc = (": " + s["description"]) if s["description"] else ""
        schema_string = f"{s['s_name']}{desc} <small>({s['size_plus_indexes']})</small>"
        s_data = {schema_string: []}
        for t in table_data:
            if t["s_name"] != s["s_name"]:
                continue
            desc = (": " + t["description"]) if t["description"] else ""
            table_string = f"<strong>{t['t_name']}</strong>:" 
            table_string += f" - <em>{t['size_plus_indexes']}, {t['rows']} rows</em> - "
            table_string += desc
            t_data = {table_string: []}
            for c in column_data:
                if c["t_name"] != t["t_name"] or c["s_name"] != s["s_name"]:
                    continue
                desc = (" " + c["description"]) if c["description"] else ""
                column_string = (
                    f"{c['column_name']}{desc} <small>({c['data_type']})</small>"
                )
                t_data[table_string].append(column_string)
            s_data[schema_string].append(t_data)
        nested_dd.append(s_data)

    save_json(nested_dd, 'table_tree')


def view_tree():
    """Generates the table tree structure.

    FIXME: Figure out how to build this data better, too much HTML mixed in here.
    """
    schema_data = schemas()
    table_data = views()
    column_data = columns()

    nested_dd = []
    for s in schema_data:
        #print(s)
        desc = (": " + s["description"]) if s["description"] else ""
        schema_string = f"{s['s_name']}{desc}"
        s_data = {schema_string: []}
        for t in table_data:
            if t["s_name"] != s["s_name"]:
                continue
            desc = (": " + t["description"]) if t["description"] else ""
            table_string = f"<strong>{t['v_name']}</strong>:" 
            table_string += desc
            t_data = {table_string: []}
            for c in column_data:
                if c["t_name"] != t["v_name"] or c["s_name"] != s["s_name"]:
                    continue
                desc = (" " + c["description"]) if c["description"] else ""
                column_string = (
                    f"{c['column_name']}{desc} <small>({c['data_type']})</small>"
                )
                t_data[table_string].append(column_string)
            s_data[schema_string].append(t_data)
        nested_dd.append(s_data)

    save_json(nested_dd, 'view_tree')

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
        self.generated_at = self.tstamp()

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

    def json(self):
        """Saves class attributes into db_stats for use.
        """
        # Cannot stuff the version object in, .public seems to be the best option.
        pgdd_version = self.pgdd_version.public
        data = {'pgdd_version': pgdd_version,
                'pg_version_full': self.pg_version_full,
                'pg_version_short': self.pg_version_short,
                'pg_host': self.pg_host,
                'pg_port': self.pg_port,
                'pg_db': self.pg_db,
                'generated_at': self.generated_at
            }
        save_json(data=data, out_name='db_stats')

    def tstamp(self):
        """Formats timestamp for display in the footer.

        Returns
        --------------------
        formatted : str
            Formatted timestamp in mm/dd/YYYY HH:MM:SS format.
        """
        now = datetime.datetime.now()
        formatted = date_time = now.strftime("%m/%d/%Y %H:%M:%S")
        return formatted