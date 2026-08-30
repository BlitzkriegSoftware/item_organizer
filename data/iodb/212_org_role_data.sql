truncate table {schema}.org_role;

INSERT INTO {schema}.org_role(
	org_role_id, description)
	VALUES (0, 'none');

INSERT INTO {schema}.org_role(
	org_role_id, description)
	VALUES (1, 'viewer');

INSERT INTO {schema}.org_role(
	org_role_id, description)
	VALUES (2, 'commenter');

INSERT INTO {schema}.org_role(
	org_role_id, description)
	VALUES (4, 'editor');

INSERT INTO {schema}.org_role(
	org_role_id, description)
	VALUES (8, 'owner');

