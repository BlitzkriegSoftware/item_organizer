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
    TDEX text := '';
    TSYM text := '';
    v_sql text := '';
	row_record RECORD;
BEGIN
    -- clear out visualization
    delete from {schema}.item_state_fsm_visualizer where org_id = target_org_id;

    SELECT count(*) INTO CT 
    FROM {schema}.item_state 
    WHERE org_id = target_org_id;

    -- create and set top row and data rows
    insert into {schema}.item_state_fsm_visualizer (row_id, label) values (0,'states');
    FOR row_record IN
        select item_state_id, state_title, ROW_NUMBER() OVER(order by item_state_id) as row_num from {schema}.item_state where org_id = target_org_id
    LOOP
        SELECT LPAD(cast(row_record.row_num as text), 2, '0') into TDEX;
		SELECT format('%s: %s', row_record.item_state_id, row_record.state_title) into TITLE;
        v_sql := 'update {schema}.item_state_fsm_visualizer set ' || format('col_%s = ', TDEX) || quote_literal(TITLE)  || ' where row_id = 0 and org_id = ' || quote_literal(target_org_id);
        EXECUTE v_sql;

        v_sql = 'Insert into {schema}.item_state_fsm_visualizer (row_id, label, org_id) values (' || row_record.row_num || ', ' || quote_literal(format('%s: %s', TDEX, row_record.state_title)) || ',' || quote_literal( target_org_id ) || ')';
        EXECUTE v_sql;
    END LOOP;

    -- raise notice 'Creating Temp Table: temp_item_order';
	DROP TABLE IF EXISTS temp_item_order;
    CREATE TEMP TABLE temp_item_order (
		item_state_id integer,
		row_num integer
	);

	-- raise notice 'filling: temp_item_order';
	insert into temp_item_order (item_state_id, row_num)
	select  item_state_id, ROW_NUMBER() OVER(order by item_state_id) as row_num
	from {schema}.item_state
	where org_id = target_org_id
	order by item_state_id;

    -- Now do the FSM
    FOR row_record IN
        select item_state_from_id, item_state_to_id from {schema}.item_state_fsm where org_id = target_org_id order by item_state_from_id, item_state_to_id
    Loop
        -- find the row index
        IRIX := 0;
		select row_num into IRIX from temp_item_order where (item_state_id = row_record.item_state_from_id);
        -- find the col index
		IVAL := 0;
  	    select row_num into IVAL from temp_item_order where (item_state_id = row_record.item_state_to_id);
		-- set the symbol
        TSYM := '>';
        IF row_record.item_state_from_id > row_record.item_state_to_id THEN
            TSYM := '<';
        END IF;

		raise notice '% IRIX=% => % IVAL=%', row_record.item_state_from_id, IRIX, row_record.item_state_to_id, IVAL;

        SELECT LPAD(cast(IVAL as text), 2, '0') into TDEX;
        v_sql := 'update {schema}.item_state_fsm_visualizer set ' || format( 'col_%s', TDEX ) || ' = ' || 
		quote_literal(TSYM) || 
		' where row_id = ' || IRIX || ' and org_id = ' || quote_literal(target_org_id); 
        EXECUTE v_sql;
    END LOOP;

    RAISE NOTICE 'FSM Visualization in Table {schema}.item_state_fsm_visualizer';
END;
$BODY$;

ALTER PROCEDURE {schema}.visualize_fsm(uuid)
    OWNER TO postgres;
