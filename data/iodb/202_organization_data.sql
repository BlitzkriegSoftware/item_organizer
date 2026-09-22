TRUNCATE TABLE {schema}.organization;

-- Required Root Organization
INSERT INTO {schema}.organization(
	org_id, parent_org_id, name)
	OVERRIDING SYSTEM VALUE 
	VALUES (0, 0, 'root organization');

-- Mostly ignored sub-org
INSERT INTO {schema}.organization(
	org_id, parent_org_id, name)
	OVERRIDING SYSTEM VALUE 
	VALUES (1, 0, 'child1');

-- Reset Next Identity
SELECT setval(
	pg_get_serial_sequence('{schema}.organization', 'org_id'), 
	coalesce(max(org_id), 1), 
	max(org_id) IS NOT NULL)
FROM {schema}.organization;
