truncate table {schema}.item_kind;

INSERT INTO {schema}.item_kind(item_kind_id, caption, notes) VALUES 
(100,'Epic','Scrum Top Level');
INSERT INTO {schema}.item_kind(item_kind_id, caption, notes) VALUES 
(110,'Feature','Scrum 2nd Level');
INSERT INTO {schema}.item_kind(item_kind_id, caption, notes) VALUES 
(120,'Impulse', 'Scrum 3rd Level');

INSERT INTO {schema}.item_kind(item_kind_id, caption, notes) VALUES 
(200,'Area','Support Top Level');
INSERT INTO {schema}.item_kind(item_kind_id, caption, notes) VALUES 
(210,'Stream','Support 2nd Level');
INSERT INTO {schema}.item_kind(item_kind_id, caption, notes) VALUES 
(220,'Focus','Support 3rd Level');

INSERT INTO {schema}.item_kind(item_kind_id, caption, notes) VALUES 
(500,'Bug','Defect, Problem, etc.');
INSERT INTO {schema}.item_kind(item_kind_id, caption, notes) VALUES 
(510,'Request', 'Feature, TODO, Task, etc.');
INSERT INTO {schema}.item_kind(item_kind_id, caption, notes) VALUES 
(520,'Activity', 'QA, DevOps, InfoSec, etc.');
INSERT INTO {schema}.item_kind(item_kind_id, caption, notes) VALUES 
(530,'Documentation','Documentation');
