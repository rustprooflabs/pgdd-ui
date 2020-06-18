-- Group role to apply permissions to.
CREATE ROLE dd_ui WITH NOLOGIN;
COMMENT ON ROLE dd_ui IS 'Group role to grant permissions needed by PgDD UI webapp.';


-- Login role for webapp access.
CREATE ROLE dd_ui_app
    WITH LOGIN PASSWORD 'UseGo0dPasswordsEverywhere'
    IN ROLE dd_ui;

COMMENT ON ROLE dd_ui IS 'Login role for PgDD UI webapp.';

--Assign permissions
REVOKE CREATE ON SCHEMA public FROM dd_ui;
REVOKE CREATE ON SCHEMA public FROM dd_ui_app;

GRANT USAGE ON SCHEMA dd_ui TO dd_ui;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA dd_ui TO dd_ui;
ALTER DEFAULT PRIVILEGES IN SCHEMA dd_ui GRANT EXECUTE ON FUNCTIONS TO dd_ui;
