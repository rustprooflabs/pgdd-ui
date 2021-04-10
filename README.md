# PgDD-UI

Generates Postgres Data Dictionary as static website using the
[PgDD extension](https://github.com/rustprooflabs/pgdd).
Provides documentation covering schemas, tables, views, functions and columns
in a user-friendly, SQL-not-required interface.  This makes sharing the database's
documentation with all business users a breeze.

> Warning: Breaking changes made after commit `b256da7` (v0.2) in order to better support PgDD v0.4 (pgx rewrite).  Use `sqitch revert` to remove the legacy PgDD-UI database objects and re-deploy from scratch.


## Requirements

Requires PostgreSQL with the [PgDD (v0.4+) extension installed](https://github.com/rustprooflabs/pgdd).  The PgDD extension is installed per-database (true for all
Postgres extensions) so the PgDD-UI is also scoped per-database.

```
psql -c "CREATE DATABASE dd_dev;"
psql -d dd_dev -c "CREATE EXTENSION IF NOT EXISTS pgdd;"
```

Python 3.7+ should work.


## Deploy Additional UI requirements

The PgDD UI generator requires additional database funtions in the ``dd_ui`` schema
to allow easily controlling webapp permissions to the PgDD schema
without interfering with any other permissions within
the database.

Uses [sqitch](https://sqitch.org/) for deployments.


```
sudo apt install sqitch
cd /path/to/pgdd-ui/db
sqitch deploy db:pg:dd_dev
```

Example of deploying to non-local Postgres instance.

```
sqitch deploy db:pg://your_db_user@db_host_or_ip/dd_dev
```

## DB Roles

Create a role for PgDD UI to use.  See `db/permissions/roles.sql`
and CHANGE THE PASSWORD!  The roles script creates Postgres group role `dd_ui`
and `dd_ui_app` login role in `dd_ui` group.

> Do NOT run the `roles.sql` script as-is and use the password included in this PUBLIC repo!

Run `perms_dd_ui.sql` to apply permissions to the group role.
Run when needed.

```
psql -d dd_dev -f db/permissions/perms_dd_ui.sql
```

## Run PgDD-UI

These instructions assume saving Python 3.7+ envs under `~/venv` and this project's
git repo is at an arbitrary `/path/to/pgdd-ui`.


```bash
cd ~/venv
python3.7 -m venv pgdd
source ~/venv/pgdd/bin/activate
```

Ensure environment is active and install requirements.

```bash
source ~/venv/pgdd/bin/activate
cd /path/to/pgdd-ui
pip install -r requirements.txt
```


Setup file with environment variables for PgDD UI to connect to DB.

```
touch ~/.pgddui
chmod 0600 ~/.pgddui
nano ~/.pgddui
```

Define the DB connection values and path to build.  `PGDD_BUILD_PATH` is optional,
leaving it out will build to a local `_build` path. 

```
DB_HOST=pg_host_or_ip
DB_NAME=dd_dev
DB_USER=dd_ui_app
DB_PW=UseGo0dPasswordsEverywhere
PGDD_BUILD_PATH=/data/pgdd/dd_dev
```

Activate venv and make environment vars available to Python.  Build the site.

```bash
source ~/venv/pgdd/bin/activate
cd /path/to/pgdd-ui
env $(cat ~/.pgddui | grep -v ^# | xargs) python build.py
```

