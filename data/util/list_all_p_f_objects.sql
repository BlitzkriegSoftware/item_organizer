SELECT 
    n.nspname AS schema_name,
    p.proname AS routine_name,
    CASE p.prokind
        WHEN 'p' THEN 'Procedure'
        WHEN 'f' THEN 'Function'
        WHEN 'a' THEN 'Aggregate'
        WHEN 'w' THEN 'Window'
    END AS routine_type,
    pg_catalog.pg_get_function_arguments(p.oid) AS arguments
FROM pg_catalog.pg_proc p
JOIN pg_catalog.pg_namespace n ON n.oid = p.pronamespace
WHERE n.nspname = 'pg_catalog'
ORDER BY routine_type, routine_name;