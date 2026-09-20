DROP PROCEDURE IF EXISTS {schema}.user_force_remove(text);

CREATE OR REPLACE PROCEDURE {schema}.user_force_remove(
    email_to_remove text
)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    owner_id bigint = 0;
    row_record RECORD; 
    inner_row_record RECORD; 
    msg text;
BEGIN

    FOR row_record IN 
        select user_id from {schema}.user 
        where email = email_to_remove
    LOOP

        IF row_record.user_id > 0 THEN

            FOR inner_row_record IN
                select item_id from {schema}.item
                    where 
                        created_by = row_record.user_id
                    or
                        assigned_to = row_record.user_id 
            LOOP
                msg = CONCAT("Reassigned to (system) from ", email_to_remove);
                CALL {schema}.item_history_add(item_id, msg);
            END LOOP;

            update {schema}.item 
                set created_by = owner_id
                where created_by = row_record.user_id;
            update {schema}.item 
                set assigned_to = owner_id
                where assigned_to = row_record.user_id;
            delete from {schema}.user_org 
                where user_id = row_record.user_id;
            delete from {schema}.user
                where user_id = row_record.user_id;
        ELSE
            RAISE EXCEPTION 'You can not remove root user!';
        END IF; -- user_id > 0
    END LOOP;
END;
$BODY$
;

ALTER PROCEDURE {schema}.user_force_remove(text)
    OWNER TO postgres;
