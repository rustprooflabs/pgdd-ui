-- Revert pgdd-ui:003 from pg

BEGIN;


CREATE OR REPLACE FUNCTION dd_ui.get_functions()
 RETURNS TABLE(s_name name, f_name name, result_data_types text, argument_data_types text, proc_security text, access_privileges text, proc_language name, description text, system_object boolean)
 LANGUAGE sql
 SECURITY DEFINER
 SET search_path TO 'dd_ui, pg_temp'
AS $function$

        SELECT s_name, f_name, result_data_types, argument_data_types, proc_security, 
                access_privileges, proc_language, description,
                system_object
            FROM dd.functions 
        ;

    $function$
;


DROP FUNCTION dd_ui.get_columns();
CREATE FUNCTION dd_ui.get_columns()
 RETURNS TABLE(type text, s_name name, t_name name, "position" smallint, column_name name, data_type name, description text, data_source text, sensitive boolean, system_object boolean)
 LANGUAGE sql
 SECURITY DEFINER
 SET search_path TO 'dd_ui, pg_temp'
AS $function$

        SELECT type, s_name, t_name, position, column_name, data_type, 
                description, data_source, sensitive,
                system_object
            FROM dd.columns
        ;

    $function$
;


DROP FUNCTION dd_ui.get_schemas();
CREATE FUNCTION dd_ui.get_schemas()
 RETURNS TABLE(s_name name, description text, table_count bigint, view_count bigint, function_count bigint, size_pretty text, size_plus_indexes text, size_bytes numeric, data_source text, sensitive boolean, system_object boolean)
 LANGUAGE sql
 SECURITY DEFINER ROWS 25
 SET search_path TO 'dd_ui, pg_temp'
AS $function$

        SELECT s_name,
                description, table_count,
                view_count, function_count,
                size_pretty, size_plus_indexes,
                size_bytes, data_source, sensitive,
                system_object
            FROM dd.schemas
        ;

    $function$
;

DROP FUNCTION dd_ui.get_tables();
CREATE FUNCTION dd_ui.get_tables()
 RETURNS TABLE(s_name name, t_name name, type text, description text, size_pretty text, size_plus_indexes text, size_bytes bigint, data_source text, sensitive boolean, system_object boolean, rows bigint)
 LANGUAGE sql
 SECURITY DEFINER ROWS 500
 SET search_path TO 'dd_ui, pg_temp'
AS $function$

        SELECT s_name, t_name, type,
                description, size_pretty, size_plus_indexes,
                size_bytes, data_source, sensitive,
                system_object,
                rows::BIGINT
            FROM dd.tables
        ;

    $function$
;


COMMIT;
