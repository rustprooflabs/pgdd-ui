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

def get_object_list(object_type):
    object_type = object_type.lower()

    if object_type == 'schemas':
        return _schemas()
    if object_type == 'tables':
        return _tables()
    if object_type == 'views':
        return _views()
    if object_type == 'columns':
        return _columns()
    if object_type == 'functions':
        return _functions()
    raise TypeError('Invalid object_type for listing.')

def _schemas():
    """Queries database for schema level details.
    """
    params = {'system_objects': get_system_objects()}
    sql_raw = 'SELECT * FROM dd_ui.get_schemas() '
    sql_raw += ' WHERE system_object = %(system_objects)s'
    sql_raw += ' ORDER BY s_name'
    return db.get_dataframe(sql_raw, params)

def _tables():
    """Queries database for table details.
    """
    sql_raw = 'SELECT * FROM dd_ui.get_tables() '
    sql_raw += ' ORDER BY s_name, t_name'
    return db.get_dataframe(sql_raw)

def _views():
    """Queries database for view details.
    """
    sql_raw = 'SELECT * FROM dd_ui.get_views() '
    sql_raw += ' ORDER BY s_name, v_name'
    return db.get_dataframe(sql_raw)


def _columns():
    """Queries database for column details for views and tables.
    """
    sql_raw = 'SELECT * FROM dd_ui.get_columns() '
    sql_raw += ' ORDER BY s_name, t_name, position'
    return db.get_dataframe(sql_raw)

def _functions():
    """Queries database for function details.
    """
    sql_raw = 'SELECT * FROM dd_ui.get_functions() '
    sql_raw += ' ORDER BY s_name, f_name'
    return db.get_dataframe(sql_raw)

