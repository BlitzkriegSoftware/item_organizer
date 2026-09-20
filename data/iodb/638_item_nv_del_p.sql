DROP PROCEDURE IF EXISTS {schema}.item_nv_del(bigint,text);

CREATE OR REPLACE PROCEDURE {schema}.item_nv_del(
    desired_item_id bigint,
    kv_key_to_remove text
)
LANGUAGE 'plpgsql'
AS $BODY$
BEGIN
    
    delete from {schema}.item_nv it 
    where (
        (it.item_id = desired_item_id) and
        (it.nv_key = kv_key_to_remove)
    );
    
END; 
$BODY$
;


ALTER PROCEDURE {schema}.item_nv_del(bigint, text)
    OWNER TO postgres;