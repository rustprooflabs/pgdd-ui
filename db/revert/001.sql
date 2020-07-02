-- Revert pgdd-ui:001 from pg

BEGIN;

	DROP SCHEMA dd_ui CASCADE;

COMMIT;
