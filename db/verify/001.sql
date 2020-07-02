-- Verify pgdd-ui:001 on pg

BEGIN;

	-- Ensure schema exists
	SELECT pg_catalog.has_schema_privilege('dd_ui', 'usage');


ROLLBACK;
