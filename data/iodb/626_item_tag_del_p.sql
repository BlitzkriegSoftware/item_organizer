DROP PROCEDURE IF EXISTS {schema}.item_tag_del(bigint,text);

CREATE OR REPLACE PROCEDURE {schema}.item_tag_del(
    desired_item_id bigint,
    tag_to_remove text
)
 LANGUAGE 'sql'
AS $BODY$
    delete from {schema}.item_tag it where (
        (it.item_id = desired_item_id) and
        (it.tag = tag_to_remove)
    );
$BODY$
;

ALTER PROCEDURE {schema}.item_tag_del(bigint, text)
    OWNER TO postgres;