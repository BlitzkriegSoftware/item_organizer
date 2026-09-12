TRUNCATE TABLE {schema}.item_history;

-- Reset Next Identity
SELECT setval(
	pg_get_serial_sequence('{schema}.item_history', 'item_history_id'), 
	coalesce(max(item_history_id), 1), 
	max(item_history_id) IS NOT NULL)
FROM {schema}.item_history;
