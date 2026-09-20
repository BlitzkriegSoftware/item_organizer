DROP PROCEDURE IF EXISTS {schema}.item_attachment_set(bigint, bigint, text, text);

CREATE OR REPLACE PROCEDURE {schema}.item_attachment_set(
    insert_item_id bigint,
    insert_user_id bigint,
    insert_caption text,
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

    INSERT INTO {schema}.item_attachment (item_id, created_by, caption, storage_url)
        VALUES ( insert_item_id, insert_user_id, insert_caption, insert_storage_url);

END; 
$BODY$
;

ALTER PROCEDURE {schema}.item_attachment_set(bigint, bigint, text, text)
    OWNER TO postgres;