# PgDD-UI

User interface to provide a user-friendly, non-SQL interface to the PostgreSQL Data Dictionary (PgDD) extension.



## Deployment Instructions

### PgDD in Docker

The PgDD extension is packaged in a Docker image
for easy testing and deployment.

```
docker pull rustprooflabs/pgdd
```

The default (`latest`) version uses PostgreSQL 12.
To pull a specific Postgres version use the tag.

```
docker pull rustprooflabs/pgdd:pg13-beta2
```

Run a container with PgDD available, this uses port `6512`.

```
docker run --name test-pgdd -e POSTGRES_PASSWORD=mysecretpassword -p 6512:5432 -d rustprooflabs/pgdd
```


### DB Development

The webapp uses functions in the `dd_ui` schema to allow
easily controlling webapp permissions to the PgDD schema
without interfering with any other permissions within
the database.

```
sudo apt install sqitch
cd /path/to/pgdd-ui/db
psql -c "CREATE DATABASE dd_dev;"
psql -d dd_dev -c "CREATE EXTENSION IF NOT EXISTS pgdd;"
sqitch deploy db:pg:dd_dev
```

Example of deploying to non-local Postgres instance.

```
sqitch deploy db:pg://your_db_user@db_host_or_ip/dd_dev
```

#### DB Roles

See `db/permissions/perms_dd_ui.sql`.

Creates Postgres group role `dd_ui` with permissions granted, and `dd_ui_app` login
role in `dd_ui` group.


### App Development

Assumes Python envs are saved under `~/venv` and git repo is
linked via VirtualBox shared folder path `/media/sf_git/pgdd-ui`.


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

Define the DB connection values.

```
DB_HOST=pg_host_or_ip
DB_NAME=dd_dev
DB_USER=dd_ui_app
DB_PW=UseGo0dPasswordsEverywhere
```

Activate venv and make environment vars available to Python.

```bash
source ~/venv/pgdd/bin/activate
cd /path/to/pgdd-ui
env $(cat ~/.pgddui | grep -v ^# | xargs) python run_server.py
```


