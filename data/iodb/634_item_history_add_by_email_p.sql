DROP PROCEDURE IF EXISTS {schema}.item_history_add_by_email(bigint,text,text,timestamp with time zone);

CREATE OR REPLACE PROCEDURE {schema}.item_history_add_by_email(
    history_item_id bigint,
    history_note text,
    history_by text = '(system)',
    history_date timestamp with time zone = now()
)
LANGUAGE 'plpgsql'
AS $BODY$

BEGIN
    insert into {schema}.item_history(item_id, created_date, created_by, note)
    values (history_item_id, history_date, history_by, history_note);
END;
$BODY$;

ALTER PROCEDURE {schema}.item_history_add_by_email(bigint, text, text, timestamp with time zone)
    OWNER TO postgres;