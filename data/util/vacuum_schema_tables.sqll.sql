SELECT format('VACUUM ANALYZE %I.%I;', table_schema, table_name) AS execute_these_commands
FROM information_schema.tables
WHERE table_schema = 'myio' AND table_type = 'BASE TABLE';
