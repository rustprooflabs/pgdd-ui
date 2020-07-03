-- Group role to apply permissions to.
CREATE ROLE dd_ui WITH NOLOGIN;
COMMENT ON ROLE dd_ui IS 'Group role to grant permissions needed by PgDD UI webapp.';


-- Login role for webapp access.
CREATE ROLE dd_ui_app
    WITH LOGIN PASSWORD 'UseGo0dPasswordsEverywhere'
    IN ROLE dd_ui;

COMMENT ON ROLE dd_ui IS 'Login role for PgDD UI webapp.';
