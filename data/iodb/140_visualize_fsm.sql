--DROP PROCEDURE {schema}.visualize_fsm(uuid);

CREATE OR REPLACE PROCEDURE {schema}.visualize_fsm(
    IN target_org_id uuid DEFAULT '00000000-0000-0000-0000-000000000000'
)
LANGUAGE 'plpgsql'
AS $BODY$

DECLARE
    I integer := 0;
    CT integer := 0;
    HSH text := '';
    TN text := '';
    TITLE text := '';
    IVAL integer := 0;
    IRIX integer := 0;
    TSYM text := '';
    v_sql text := '';
	row_record RECORD;
BEGIN
    SELECT count(*) INTO CT 
    FROM {schema}.item_state 
    WHERE org_id = target_org_id;

    select {schema}.uuid_to_short(target_org_id) into HSH;
    select 'FSM' || HSH into TN;
    -- 0, index, 1: title, ... values
    PERFORM {schema}.create_dynamic_table(TN, CT + 2);
	TN := 'public.' || TN;

    -- make the empty rows
    IVAL := CT + 1;
    FOR I IN 0..IVAL LOOP
      v_sql := 'insert into ' || TN || '(col_1) values (' || cast(I as TEXT) || ')';
      EXECUTE v_sql;
    END LOOP;

    -- Top Row
    I := 3;
    FOR row_record IN 
        select item_state_id from {schema}.item_state where org_id = target_org_id order by item_state_id
    LOOP
        IVAL := row_record.item_state_id;
        v_sql := 'update ' || TN || ' set ' || format('col_%s = %s', i, IVAL) || ' where col_1 = 0 ';
        EXECUTE v_sql;
        I := I + 1; 
    END LOOP;

    -- column labels
    FOR row_record IN
        select item_state_id, state_title, ROW_NUMBER() OVER(order by item_state_id) as row_num 
		from {schema}.item_state 
		where org_id = target_org_id 
    LOOP
        IRIX := row_record.row_num;
        TITLE := row_record.state_title;
        v_sql := 'update ' || TN || ' set col_2 = ' || TITLE || ' where COL_1 = ' || IRIX ;
        EXECUTE v_sql;
    END LOOP;

    -- Now do the FSM
    FOR row_record IN
        select item_state_from_id, item_state_to_id from {schema}.item_state_fsm where org_id = target_org_id order by item_state_from_id, item_state_to_id
    Loop
        -- find the row index
        select  ROW_NUMBER() OVER(order by item_state_id) into IRIX from {schema}.item_state where (org_id = target_org_id) and (item_state_id = row_record.item_state_from_id);
        -- find the col index
        select  ROW_NUMBER() OVER(order by item_state_id) into IVAL from {schema}.item_state where (org_id = target_org_id) and (item_state_id = row_record.item_state_to_id);
        -- do the update
        TSYM := '>';
        IF row_record.item_state_from_id > row_record.item_state_to_id THEN
            TSYM := '<';
        END IF;
        v_sql := 'update ' || TN || ' set ' || format('col_%s = %s', IVAL + 2, TSYM) || ' where ' || format('col_1 = %s', IRIX);
        EXECUTE v_sql;
    END LOOP;

    RAISE NOTICE 'FSM Visualization in Table %s', TN;
END;
$BODY$;

ALTER PROCEDURE {schema}.visualize_fsm(uuid)
    OWNER TO postgres;
