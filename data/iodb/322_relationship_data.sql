truncate table {schema}.relationship;

INSERT INTO {schema}.relationship(
	relationship_id, reciprocal_relationship_id, relationship_title, notes)
	VALUES (10, 10,'Related', 'misc. relationship');

INSERT INTO {schema}.relationship(
	relationship_id, reciprocal_relationship_id, relationship_title, notes)
	VALUES(20, 30,'Predecessor', 'happens before this one');

INSERT INTO {schema}.relationship(
	relationship_id, reciprocal_relationship_id, relationship_title, notes)
	VALUES(30, 20,'Successor', 'happens after this one');

INSERT INTO {schema}.relationship(
	relationship_id, reciprocal_relationship_id, relationship_title, notes)
	VALUES(40, 50, 'Parent', 'holds this one');

INSERT INTO {schema}.relationship(
	relationship_id, reciprocal_relationship_id, relationship_title, notes)
	VALUES(50, 40, 'Child', 'is held by this one');
