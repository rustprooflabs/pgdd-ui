import logging
from flask import render_template, abort, jsonify
import psycopg2.extras
from webapp import app, pgdd, db

LOGGER = logging.getLogger(__name__)


@app.route("/") # Hard coding default route
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
    with db.get_db_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute("select * from dd_ui.get_columns() order by column_name")
            columns = cursor.fetchall()
            cursor.execute("select * from dd_ui.get_tables() order by t_name")
            tables = cursor.fetchall()
            cursor.execute("select * from dd_ui.get_schemas() order by s_name")
            schemas = cursor.fetchall()

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


