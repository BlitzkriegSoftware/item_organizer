CREATE OR REPLACE PROCEDURE {schema}.item_history_add(
    history_item_id bigint,
    history_note text,
    history_by uuid = '00000000-0000-0000-0000-000000000000',
    history_date timestamp with time zone = now()
)
LANGUAGE 'plpgsql'
AS $BODY$

DECLARE
    history_id uuid = gen_random_uuid();

BEGIN
    insert into {schema}.item_history(id, item_id,created_date, created_by, note)
    values (history_id, history_item_id, history_date, history_by, history_note);
END;
$BODY$;

ALTER PROCEDURE {schema}.item_history_add(bigint, text, uuid, timestamp with time zone)
    OWNER TO postgres;