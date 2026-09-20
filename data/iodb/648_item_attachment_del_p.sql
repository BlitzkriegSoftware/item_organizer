DROP PROCEDURE IF EXISTS {schema}.item_attachment_del(bigint, text);

CREATE OR REPLACE PROCEDURE {schema}.item_attachment_del(
    insert_item_id bigint,
    insert_storage_url text
)
LANGUAGE 'plpgsql'
AS $BODY$

DECLARE
    work text := '';
BEGIN

    DELETE FROM {schema}.item_attachment
    WHERE (
        storage_url = insert_storage_url
    ) AND (item_id = insert_item_id);

END; 
$BODY$
;

ALTER PROCEDURE {schema}.item_attachment_del(bigint, text)
    OWNER TO postgres;