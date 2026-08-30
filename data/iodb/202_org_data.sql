-- Required Root Organization

INSERT INTO {schema}.organization(
	org_id, parent_org_id, name)
	VALUES ('00000000-0000-0000-0000-000000000000', null, 'root organization');