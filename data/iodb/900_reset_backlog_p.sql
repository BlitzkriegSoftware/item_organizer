-- RESET ALL ITEM Data
-- This is the nucular option

DROP PROCEDURE IF EXISTS {schema}.reset_backlog();

CREATE OR REPLACE PROCEDURE {schema}.reset_backlog()
LANGUAGE 'plpgsql'
AS $BODY$

BEGIN

    truncate table {schema}.item_history;
    truncate table {schema}.item_tag;
    truncate table {schema}.item;

    ALTER SEQUENCE {schema}.item_item_id_seq RESTART WITH 1;

END;
$BODY$;

ALTER PROCEDURE {schema}.reset_backlog()
    OWNER TO postgres;
