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
