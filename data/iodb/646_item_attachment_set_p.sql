DROP PROCEDURE IF EXISTS {schema}.item_attachment_set(bigint, bigint, text, text, text);

CREATE OR REPLACE PROCEDURE {schema}.item_attachment_set(
    insert_item_id bigint,
    insert_user_id bigint,
    insert_caption text,
    insert_storage_url text,
    insert_file_hash text
)
LANGUAGE 'plpgsql'
AS $BODY$

DECLARE
    work text := '';
BEGIN

    IF NULLIF(my_text, '') IS NULL THEN
        work := CONCAT_WS(insert_caption, insert_storage_url);
        insert_file_hash := encode(sha512(work), 'hex');
    END IF;

    DELETE FROM {schema}.item_attachment
    WHERE (
        file_hash = insert_file_hash
        OR
        storage_url = insert_storage_url
    ) AND (item_id = insert_item_id);

    INSERT INTO {schema}.item_attachment (item_id, created_by, caption, storage_url, file_hash)
        VALUES ( insert_item_id, insert_user_id, insert_caption, insert_storage_url, insert_file_hash);

END; 
$BODY$
;

ALTER PROCEDURE {schema}.item_attachment_set(bigint, bigint, text, text, text)
    OWNER TO postgres;