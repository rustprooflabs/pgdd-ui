"""PgDD UI Builder module."""
import os
from pgdd_ui import pgdd, config

def run():
    """Runs the pgdd_ui.builder module"""
    print("Running PgDD builder...")
    db_stats = pgdd.DatabaseStats()

    _save_pgdd_data()
    _print_db_stats(db_stats)
    _build_db_index(db_stats)
    _build_schema_list(db_stats)


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
    out_dir = config.BUILD_PATH
    _ensure_dir_exists(out_dir)
    pgdd.schemas()
    pgdd.tables()
    pgdd.views()
    pgdd.functions()
    pgdd.columns()


def _build_db_index(db_stats):
    template = config.J2_ENV.get_template('index.j2.html')

    rendered = template.render(db_stats=db_stats)
    save_rendered_template(out_name='index.html', content=rendered)


def _build_schema_list(db_stats):
    """Renders schema list page.

    Parameters
    -------------------------
    db_stats : pgdd.DatabaseStats
    """
    template = config.J2_ENV.get_template('schema_list.j2.html')

    schemas = 'Coming soon!'
    rendered = template.render(db_stats=db_stats,
                               schemas=schemas)
    save_rendered_template(out_name='schemas.html', content=rendered)



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

