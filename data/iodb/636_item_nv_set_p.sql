DROP PROCEDURE IF EXISTS {schema}.item_nv_set(bigint,text,text);

CREATE OR REPLACE PROCEDURE {schema}.item_nv_set(
    desired_item_id bigint,
    new_nv_key text,
    new_nv_value text
)
 LANGUAGE 'sql'
AS $BODY$
    new_nv_value := TRIM(new_nv_value)
    delete from {schema}.item_nv it 
    where (
        (it.item_id = desired_item_id) and
        (it.nv_key = new_nv_key)
    );
    IF (LENGTH(new_nv_value) > 0) THEN
        insert into {schema}.item_nv (item_id, nv_key, nv_value) 
        values (desired_item_id, new_nv_key, new_nv_value);
    END IF;
$BODY$
;

ALTER PROCEDURE {schema}.item_nv_set(bigint, text, text)
    OWNER TO postgres;