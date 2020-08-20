import logging
from flask import session
from packaging.version import parse as parse_version
from webapp import config, db


LOGGER = logging.getLogger(__name__)


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
                              return_format='RealDict',
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


def set_system_objects(system_objects):
    """Sets system_objects flag in session.

    Parameters
    -------------------------
    system_objects : bool
    """
    msg = f'Setting system_objects session value: {system_objects}'
    LOGGER.debug(msg)
    session['system_objects'] = system_objects
    if system_objects:
        session['system_objects_lower'] = 'true'
    else:
        session['system_objects_lower'] = 'false'
    session.modified = True


def get_system_objects():
    """Retrieves system_objects flag in session.

    Uses default value from `set_system_objects()` if not
    previously set.

    Returns
    -------------------------
    system_objects : bool
    """
    system_objects = session.get('system_objects')
    if system_objects is None:
        msg = 'system_objects not previously set.  Setting to default.'
        LOGGER.info(msg)
        set_system_objects(False)
        system_objects = session.get('system_objects')

    return system_objects


def get_object_list(object_type, return_format='DataFrame'):
    """Returns the list for objects of `object_type`.

    Parameters
    -------------------
    object_type : str
        e.g. schemas, tables, etc.

    return_format : str
        Options:
            * DataFrame (Default)
            * RealDict 
    """
    object_type = object_type.lower()

    if object_type == 'schemas':
        return _schemas(return_format=return_format)
    if object_type == 'tables':
        return _tables(return_format=return_format)
    if object_type == 'views':
        return _views(return_format=return_format)
    if object_type == 'columns':
        return _columns(return_format=return_format)
    if object_type == 'functions':
        return _functions(return_format=return_format)
    raise TypeError('Invalid object_type for listing.')

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

def _schemas(return_format):
    """Queries database for schema level details.
    """
    sql_raw = 'SELECT * FROM dd_ui.get_schemas() '
    sql_raw += ' WHERE system_object = %(system_objects)s '
    sql_raw += ' ORDER BY s_name'
    params = {'system_objects': get_system_objects()}
    data = db.get_data(sql_raw, params, return_format)
    return data

def _tables(return_format):
    """Queries database for table details.
    """
    sql_raw = 'SELECT * FROM dd_ui.get_tables() '
    sql_raw += ' WHERE system_object = %(system_objects)s '
    sql_raw += ' ORDER BY s_name, t_name'
    params = {'system_objects': get_system_objects()}
    data = db.get_data(sql_raw, params, return_format)
    return data

def _views(return_format):
    """Queries database for view details.
    """
    sql_raw = 'SELECT * FROM dd_ui.get_views() '
    sql_raw += ' WHERE system_object = %(system_objects)s '
    sql_raw += ' ORDER BY s_name, v_name'
    params = {'system_objects': get_system_objects()}
    data = db.get_data(sql_raw, params, return_format)
    return data


def _columns(return_format):
    """Queries database for column details for views and tables.
    """
    sql_raw = 'SELECT * FROM dd_ui.get_columns() '
    sql_raw += ' WHERE system_object = %(system_objects)s '
    sql_raw += ' ORDER BY s_name, t_name, position'
    params = {'system_objects': get_system_objects()}
    data = db.get_data(sql_raw, params, return_format)
    return data

def _functions(return_format):
    """Queries database for function details.
    """
    sql_raw = 'SELECT * FROM dd_ui.get_functions() '
    sql_raw += ' WHERE system_object = %(system_objects)s '
    sql_raw += ' ORDER BY s_name, f_name'
    params = {'system_objects': get_system_objects()}
    data = db.get_data(sql_raw, params, return_format)
    return data

