-- Required Root Organization

INSERT INTO {schema}.organization(
	org_id, parent_org_id, name)
	VALUES ('00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000', 'root organization');

INSERT INTO myio.organization(
	org_id, parent_org_id, name)
	VALUES ('00000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000000', 'child1');
