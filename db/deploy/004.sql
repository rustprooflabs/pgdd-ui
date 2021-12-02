-- Deploy pgdd-ui:004 to pg

BEGIN;

COMMENT ON SCHEMA dd_ui IS 'Schema for PgDD user interface objects. See https://github.com/rustprooflabs/pgdd-ui';

COMMENT ON FUNCTION dd_ui.get_functions IS 'Returns details about functions within the database.';
COMMENT ON FUNCTION dd_ui.get_schemas IS 'Returns details about schemas within the database.';
COMMENT ON FUNCTION dd_ui.get_tables IS 'Returns details about tables (incl. FDW tables) within the database. Excludes Postgres catalog tables.';
COMMENT ON FUNCTION dd_ui.get_views IS 'Returns details about views (incl. mat views) within the database. Excludes Postgres catalog views.';
COMMENT ON FUNCTION dd_ui.get_columns IS 'Returns details about columns for tables and views.';


COMMIT;
