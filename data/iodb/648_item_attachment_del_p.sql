
DROP PROCEDURE IF EXISTS {schema}.item_attachment_del(bigint, text, text, text);

CREATE OR REPLACE PROCEDURE {schema}.item_attachment_del(
    insert_item_id bigint,
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

END; 
$BODY$
;

ALTER PROCEDURE {schema}.item_attachment_del(bigint, text, text, text)
    OWNER TO postgres;