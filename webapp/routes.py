import logging
from flask import abort, g, jsonify, render_template, request
import psycopg2.extras
from webapp import app, pgdd, db

LOGGER = logging.getLogger(__name__)

# Gather database level stats, restart app to refresh.
DB_STATS = pgdd.DatabaseStats()

@app.before_request
def pgdd_version_check():
    """Checks if PgDD extension will work with this webapp."""
    min_version = pgdd.min_supported_version()
    pgdd_version = pgdd.version()
    if pgdd_version < min_version:
        abort(501)

    # Set DB_STATS to global object, makes always avaiable for footer.
    g.db_stats = DB_STATS

@app.route('/_toggle_system_objects')
def toggle_system_objects():
    system_objects = request.args.get('system_objects')

    if system_objects.lower() == 'true':
        pgdd.set_system_objects(True)
    else:
        pgdd.set_system_objects(False)

    return jsonify({'status': 'success'})


@app.route("/")
def view_database_stats():
    return render_template("database.html")


@app.route("/tree")
def view_tree():
    """Displays tree view of tables within schemas.
    """
    return render_template("tree.html")


@app.route('/<object_type>')
def view_schemas_list(object_type):
    """Displays basic listing of `object_type`.
    """
    try:
        object_list = pgdd.get_object_list(object_type)
    except TypeError:
        abort(404)

    return render_template('/object_list.html',
                           object_list=object_list,
                           object_type=object_type)


@app.route("/dd.json")
def payload():
    tree_data = pgdd.get_table_tree()
    schemas = tree_data['schemas']
    tables = tree_data['tables']
    columns = tree_data['columns']

    nested_dd = []
    for s in schemas:
        #print(s)
        desc = (": " + s["description"]) if s["description"] else ""
        schema_string = f"{s['s_name']}{desc} <small>({s['size_plus_indexes']})</small>"
        s_data = {schema_string: []}
        for t in tables:
            if t["s_name"] != s["s_name"]:
                continue
            desc = (": " + t["description"]) if t["description"] else ""
            table_string = f"<strong>{t['t_name']}</strong>:" 
            table_string += f" - <em>{t['size_plus_indexes']}, {t['rows']} rows</em> - "
            table_string += desc
            t_data = {table_string: []}
            for c in columns:
                if c["t_name"] != t["t_name"] or c["s_name"] != s["s_name"]:
                    continue
                desc = (" " + c["description"]) if c["description"] else ""
                column_string = (
                    f"{c['column_name']}{desc} <small>({c['data_type']})</small>"
                )
                t_data[table_string].append(column_string)
            s_data[schema_string].append(t_data)
        nested_dd.append(s_data)

    return jsonify(nested_dd)


@app.errorhandler(404)
def page_not_found(err):
    """ Handles 404 errors to render custom 404 page """
    LOGGER.error('404 error: %s', err)
    return render_template('404.html'), 404

@app.errorhandler(501)
def outdated_pgdd_extension(err):
    """ Handles errors of outdated extension as 501 http error code."""
    min_version = pgdd.min_supported_version()
    pgdd_version = pgdd.version()
    msg = f'PgDD extension version {pgdd_version} outdated. '
    msg += f'Requires at least {min_version}'
    LOGGER.error(msg)
    return render_template('501.html', min_version=min_version,
                           pgdd_version=pgdd_version), 501

