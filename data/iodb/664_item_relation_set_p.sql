DROP PROCEDURE IF EXISTS {schema}.item_relation_set(bigint, bigint, integer);

CREATE OR REPLACE PROCEDURE {schema}.item_relation_set(
    in_from_id bigint,
    in_to_id bigint,
    in_relationship_id integer
)
LANGUAGE 'plpgsql'
AS $BODY$

DECLARE
    rec_rel_id integer = 0;
BEGIN

    -- remove relation and its reciprocal
    DELETE from {schema}.item_relation 
    WHERE from_item_id = in_from_id AND
          to_item_id = in_to_id;

    DELETE from {schema}.item_relation 
    WHERE from_item_id = in_to_id AND
          to_item_id = in_from_id;
    
    select reciprocal_relationship_id into rec_rel_id
    FROM {schema}.relationship
    WHERE relationship_id = in_relationship_id;

    IF (rec_rel_id is NULL) THEN
        RAISE EXCEPTION 'reciprocal not found'; 
    END IF;

    -- set new relation and its reciprocal
    INSERT INTO {schema}.relationship(from_item_id, to_item_id, relationship_id)
    VALUES (in_from_id, in_to_id, in_relationship_id);

    INSERT INTO {schema}.relationship(from_item_id, to_item_id, relationship_id)
    VALUES ( in_to_id, in_from_id, rec_rel_id);

END; 
$BODY$
;

ALTER PROCEDURE {schema}.item_relation_set(bigint, bigint, integer)
    OWNER TO postgres;