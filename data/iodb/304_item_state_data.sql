TRUNCATE TABLE {schema}.item_state;

INSERT INTO {schema}.item_state(
	item_state_id, state_title, org_id)
	VALUES (10, 'new', 0 );

INSERT INTO {schema}.item_state(
	item_state_id, state_title, org_id)
	VALUES (20, 'triaged', 0 );

INSERT INTO {schema}.item_state(
	item_state_id, state_title, org_id)
	VALUES (30, 'active', 0 );

INSERT INTO {schema}.item_state(
	item_state_id, state_title, org_id)
	VALUES (40, 'blocked', 0 );

INSERT INTO {schema}.item_state(
	item_state_id, state_title, org_id)
	VALUES (50, 'testable', 0 );
	
INSERT INTO {schema}.item_state(
	item_state_id, state_title, org_id)
	VALUES (60, 'releasable', 0 );
	
INSERT INTO {schema}.item_state(
	item_state_id, state_title, org_id)
	VALUES (70, 'closed', 0 );
	
INSERT INTO {schema}.item_state(
	item_state_id, state_title, org_id)
	VALUES (80, 'rejected', 0 );
	
INSERT INTO {schema}.item_state(
	item_state_id, state_title, org_id)
	VALUES (90, 'removed', 0 );
	