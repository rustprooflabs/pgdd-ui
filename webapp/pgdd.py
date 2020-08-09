from flask import session
from webapp import db


def set_system_objects(system_objects=False):
    """Sets system_objects flag in session.

    Parameters
    -------------------------
    system_objects : bool
    """
    session['system_objects'] = system_objects

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
        set_system_objects()
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

