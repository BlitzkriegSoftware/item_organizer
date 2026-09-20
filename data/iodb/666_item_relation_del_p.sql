DROP PROCEDURE IF EXISTS {schema}.item_relation_del(bigint, bigint);

CREATE OR REPLACE PROCEDURE {schema}.item_relation_del(
    in_from_id bigint,
    in_to_id bigint
)
LANGUAGE 'plpgsql'
AS $BODY$

BEGIN
    -- remove relation and its reciprocal
    DELETE from {schema}.item_relation 
    WHERE from_item_id = in_from_id AND
          to_item_id = in_to_id;

    DELETE from {schema}.item_relation 
    WHERE from_item_id = in_to_id AND
          to_item_id = in_from_id;
END; 
$BODY$
;

ALTER PROCEDURE {schema}.item_relation_del(bigint, bigint)
    OWNER TO postgres;