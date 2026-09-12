DROP PROCEDURE IF EXISTS {schema}.item_remove(bigint);

CREATE OR REPLACE PROCEDURE {schema}.item_remove(
    target_item_id bigint
)
LANGUAGE 'plpgsql'
AS $BODY$

BEGIN
    delete from {schema}.item_nv where item_id = target_item_id;
    delete from {schema}.item_tag where item_id = target_item_id;
    delete from {schema}.item_history where item_id = target_item_id;
    delete from {schema}.item where item_id = target_item_id;
END;
$BODY$;

ALTER PROCEDURE {schema}.item_remove(bigint)
    OWNER TO postgres;