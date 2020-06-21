import os

from flask import Flask, render_template, jsonify
import psycopg2
import psycopg2.extras

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dd.json")
def payload():
    POSTGRESQL_CONNECTION = os.environ["POSTGRESQL_CONNECTION"]
    with psycopg2.connect(POSTGRESQL_CONNECTION) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute("select * from dd.columns order by column_name")
            columns = cursor.fetchall()
            cursor.execute("select * from dd.tables order by t_name")
            tables = cursor.fetchall()
            cursor.execute("select * from dd.schemas order by s_name")
            schemas = cursor.fetchall()

    nested_dd = []
    for s in schemas:
        print(s)
        schema_string = f"{s['s_name']} ({s['description']}, {s['size_plus_indexes']})"
        s_data = {schema_string: []}
        for t in tables:
            if t["s_name"] != s["s_name"]:
                continue
            table_string = (
                f"{t['t_name']} ({t['description']}, {t['size_plus_indexes']})"
            )
            t_data = {table_string: []}
            for c in columns:
                if c["t_name"] != t["t_name"] or c["s_name"] != s["s_name"]:
                    continue
                column_string = (
                    f"{c['column_name']} ({c['data_type']}, {c['description']})"
                )
                t_data[table_string].append(column_string)
            s_data[schema_string].append(t_data)
        nested_dd.append(s_data)

    return jsonify(nested_dd)


if __name__ == "__main__":
    app.run(debug=True)
