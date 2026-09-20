truncate table {schema}.priority;

INSERT INTO {schema}.priority(
	priority_id, priority_title, notes)
	VALUES (1, 'p1', 'Critical Need or Complete service outage or failure affecting a large number of users or a mission-critical system');

INSERT INTO {schema}.priority(
	priority_id, priority_title, notes)
	VALUES (2, 'p2','Urgent Need or Significant degradation of a key service with no viable workaround');

INSERT INTO {schema}.priority(
	priority_id, priority_title, notes)
	VALUES (3, 'p3', 'Core Need or Partial service impact with a workaround available; limited user disruption');

INSERT INTO {schema}.priority(
	priority_id, priority_title, notes)
	VALUES (4, 'p4', 'Useful Need or Minor issue with minimal business impact; cosmetic or informational');

INSERT INTO {schema}.priority(
	priority_id, priority_title, notes)
	VALUES (5, 'p5', 'Nice to have or Service Improvement');
