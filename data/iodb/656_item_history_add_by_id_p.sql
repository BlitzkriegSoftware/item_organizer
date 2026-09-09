DROP PROCEDURE IF EXISTS {schema}.item_history_add_by_id;

CREATE OR REPLACE PROCEDURE {schema}.item_history_add_by_id(
    history_item_id bigint,
    history_note text,
    history_user_id bigint = -1,
    history_date timestamp with time zone = now()
)
LANGUAGE 'plpgsql'
AS $BODY$

DECLARE
    email_text text = '(system)';
BEGIN
    select email into email_text from {schema}."user" 
       where user_id = history_user_id;
    IF NOT FOUND THEN
        email_text :='(system)'; -- Handle missing row logic here
    END IF;

    insert into {schema}.item_history(item_id, created_date, created_by, note)
    values (history_item_id, history_date, email_text, history_note);
END;
$BODY$;

ALTER PROCEDURE {schema}.item_history_add_by_id(bigint, text, bigint, timestamp with time zone)
    OWNER TO postgres;