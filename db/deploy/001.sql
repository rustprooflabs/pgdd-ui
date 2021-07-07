-- Deploy pgdd-ui:001 to pg

BEGIN;

    CREATE SCHEMA dd_ui;

    CREATE FUNCTION dd_ui.get_schemas()
     RETURNS TABLE(s_name NAME,
        description TEXT, table_count BIGINT,
        view_count BIGINT, function_count BIGINT,
        size_pretty TEXT, size_plus_indexes TEXT,
        size_bytes NUMERIC,
        data_source TEXT, sensitive BOOLEAN,
        system_object BOOLEAN)
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

    $function$;

    COMMENT ON FUNCTION dd_ui.get_schemas IS 'Returns details about schemas within a single database.';


    CREATE FUNCTION dd_ui.get_tables()
     RETURNS TABLE(s_name NAME, t_name NAME, type TEXT,
        description TEXT, size_pretty TEXT, size_plus_indexes TEXT,
        size_bytes BIGINT,
        data_source TEXT, sensitive BOOLEAN,
        system_object BOOLEAN)
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

    $function$;

    COMMENT ON FUNCTION dd_ui.get_tables IS 'Returns details about tables (incl. FDW tables) within a single database.';


    CREATE FUNCTION dd_ui.get_views()
     RETURNS TABLE(s_name NAME, v_name NAME, type TEXT,
        description TEXT, system_object BOOLEAN)
     LANGUAGE sql
     SECURITY DEFINER ROWS 500
     SET search_path TO 'dd_ui, pg_temp'
    AS $function$

        SELECT s_name, v_name, view_type AS type,
                description, system_object
            FROM dd.views
            WHERE s_name NOT IN ('pg_catalog', 'information_schema')
        ;

    $function$;

    COMMENT ON FUNCTION dd_ui.get_views IS 'Returns details about views (incl. mat views) within a single database.  Excludes Postgres catalog views by schema.';


    CREATE FUNCTION dd_ui.get_columns()
     RETURNS TABLE(source_type TEXT, s_name NAME, t_name NAME, "position" SMALLINT,
        c_name NAME, data_type NAME,
        description TEXT, data_source TEXT, sensitive BOOLEAN,
        system_object BOOLEAN)
     LANGUAGE sql
     SECURITY DEFINER ROWS 1000
     SET search_path TO 'dd_ui, pg_temp'
    AS $function$

        SELECT source_type, s_name, t_name, position, c_name, data_type,
                description, data_source, sensitive,
                system_object
            FROM dd.columns
        ;

    $function$;


    COMMENT ON FUNCTION dd_ui.get_columns IS 'Returns details about columns for one type of object at a time (e.g. `table` or `view`).';



    CREATE FUNCTION dd_ui.get_functions()
     RETURNS TABLE(s_name NAME, f_name NAME, result_data_types TEXT,
        argument_data_types TEXT, proc_security TEXT, access_privileges TEXT,
        proc_language NAME,
        description TEXT, system_object BOOLEAN)
     LANGUAGE sql
     SECURITY DEFINER ROWS 1000
     SET search_path TO 'dd_ui, pg_temp'
    AS $function$

        SELECT s_name, f_name, result_data_types, argument_data_types, proc_security, 
                access_privileges, proc_language, description,
                system_object
            FROM dd.functions 
        ;

    $function$;


COMMIT;
