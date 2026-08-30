-- RESET ALL ITEM Data
-- This is the nucular option

DROP PROCEDURE IF EXISTS {schema}.reset_backlog();

CREATE OR REPLACE PROCEDURE {schema}.reset_backlog(flag integer)
LANGUAGE 'plpgsql'
AS $BODY$

BEGIN
    IF flag >= 999 THEN
        truncate table {schema}.item_history;
        truncate table {schema}.item_tag;
        truncate table {schema}.item RESTART IDENTITY CASCADE;
        ALTER SEQUENCE {schema}.item_item_id_seq RESTART WITH 1;
    END IF;
END;
$BODY$
;

ALTER PROCEDURE {schema}.reset_backlog(integer)
    OWNER TO postgres;
