TRUNCATE TABLE {schema}.item_state;

INSERT INTO {schema}.item_state(
	item_state_id, state_title, org_id)
	VALUES (10, 'new', '00000000-0000-0000-0000-000000000000' );

INSERT INTO {schema}.item_state(
	item_state_id, state_title, org_id)
	VALUES (20, 'triaged', '00000000-0000-0000-0000-000000000000' );

INSERT INTO {schema}.item_state(
	item_state_id, state_title, org_id)
	VALUES (30, 'active', '00000000-0000-0000-0000-000000000000' );

INSERT INTO {schema}.item_state(
	item_state_id, state_title, org_id)
	VALUES (40, 'blocked', '00000000-0000-0000-0000-000000000000' );

INSERT INTO {schema}.item_state(
	item_state_id, state_title, org_id)
	VALUES 50, 'testable', '00000000-0000-0000-0000-000000000000' );
	
INSERT INTO {schema}.item_state(
	item_state_id, state_title, org_id)
	VALUES (60, 'releasable', '00000000-0000-0000-0000-000000000000' );
	
INSERT INTO {schema}.item_state(
	item_state_id, state_title, org_id)
	VALUES (70, 'closed', '00000000-0000-0000-0000-000000000000' );
	
INSERT INTO {schema}.item_state(
	item_state_id, state_title, org_id)
	VALUES (80, 'rejected', '00000000-0000-0000-0000-000000000000' );
	
INSERT INTO {schema}.item_state(
	item_state_id, state_title, org_id)
	VALUES (90, 'removed', '00000000-0000-0000-0000-000000000000' );
	