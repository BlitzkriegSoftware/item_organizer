TRUNCATE TABLE {schema}.item;

-- Reset Next Identity
SELECT setval(
	pg_get_serial_sequence('{schema}.item', 'item_id'), 
	coalesce(max(item_id), 1), 
	max(item_id) IS NOT NULL)
FROM {schema}.item;