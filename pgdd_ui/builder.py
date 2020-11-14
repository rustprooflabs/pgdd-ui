"""PgDD UI Builder module."""
import os
from pgdd_ui import pgdd, config

def run():
    """Runs the pgdd_ui.builder module"""
    print("Running PgDD builder...")

    _save_pgdd_data()
    _build_db_index()
    _build_schema_list()
    _build_table_list()
    _build_view_list()
    _build_column_list()
    _build_function_list()


def _print_db_stats(db_stats):
    """Prints helpful output to operator running the generator.

    Parameters
    --------------------
    db_stats : pgdd.DatabaseStats
    """
    print(f"Connected to: {db_stats.pg_host}/{db_stats.pg_db}")
    print(f"Postgres Version: {db_stats.pg_version_short}")
    print(f"PgDD Version: {db_stats.pgdd_version}")


def _save_pgdd_data():
    """Saves all PgDD data to JSON format in the directory `config.BUILD_PATH`.
    """
    db_stats = pgdd.DatabaseStats()
    _print_db_stats(db_stats)

    out_dir = config.BUILD_PATH
    _ensure_dir_exists(out_dir)
    db_stats.json()
    pgdd.schemas()
    pgdd.tables()
    pgdd.views()
    pgdd.functions()
    pgdd.columns()


def _build_db_index():
    template = config.J2_ENV.get_template('index.j2.html')
    rendered = template.render()
    save_rendered_template(out_name='index.html', content=rendered)


def _build_schema_list():
    """Renders schema listing page.
    """
    template = config.J2_ENV.get_template('schema_list.j2.html')
    rendered = template.render()
    save_rendered_template(out_name='schemas.html', content=rendered)


def _build_table_list():
    """Renders table listing page.
    """
    template = config.J2_ENV.get_template('table_list.j2.html')
    rendered = template.render()
    save_rendered_template(out_name='tables.html', content=rendered)


def _build_view_list():
    """Renders view listing page.
    """
    template = config.J2_ENV.get_template('view_list.j2.html')
    rendered = template.render()
    save_rendered_template(out_name='views.html', content=rendered)

def _build_column_list():
    """Renders column listing page.
    """
    template = config.J2_ENV.get_template('column_list.j2.html')
    rendered = template.render()
    save_rendered_template(out_name='columns.html', content=rendered)

def _build_function_list():
    """Renders function listing page.
    """
    template = config.J2_ENV.get_template('function_list.j2.html')
    rendered = template.render()
    save_rendered_template(out_name='functions.html', content=rendered)


def save_rendered_template(out_name, content):
    """Saves rendered `content` to build directory in `out_name` file.

    Parameters
    --------------------
    out_name : str
        Name for output filename.

    content : str
        Rendered HTML content to save to file.
    """
    out_dir = config.BUILD_PATH
    _ensure_dir_exists(out_dir)
    out_file = os.path.join(out_dir, out_name)
    with open(out_file, "w") as f:
        f.write(content)


def _ensure_dir_exists(out_dir):
    """Creates `out_dir` if does not exist.  Ignores error if already exists.

    Parameters
    -----------------
    out_dir : str
        Path of directory to ensure exists.
    """
    try:
        os.mkdir(out_dir)
    except OSError:
        pass

