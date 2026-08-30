CREATE OR REPLACE PROCEDURE {schema}.item_tag_set(
        desired_item_id bigint
        new_tag text
)
 LANGUAGE 'sql'
AS $BODY$
    delete from {schema}.item_tag it where (
        (it.item_id = desired_item_id) and
        (it.tag = new_tag)
    );
    insert into {schema}.item_tag (item_id, tag) 
    values (desired_item_id, new_tag);
$BODY$