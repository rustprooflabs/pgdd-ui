-- Revert pgdd-ui:002 from pg

BEGIN;

DROP FUNCTION dd_ui.get_tables();
CREATE FUNCTION dd_ui.get_tables()
 RETURNS TABLE(s_name name, t_name name, type text, description text, size_pretty text, size_plus_indexes text, size_bytes bigint, data_source text, sensitive boolean, system_object boolean)
 LANGUAGE sql
 SECURITY DEFINER ROWS 500
 SET search_path TO 'dd_ui, pg_temp'
AS $function$

        SELECT s_name, t_name, type,
                description, size_pretty, size_plus_indexes,
                size_bytes, data_source, sensitive,
                system_object
            FROM dd.tables
        ;

    $function$
;


COMMIT;
