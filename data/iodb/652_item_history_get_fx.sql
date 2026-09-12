DROP FUNCTION IF EXISTS {schema}.item_history_get(bigint, integer, integer);

CREATE OR REPLACE FUNCTION {schema}.item_history_get(
    history_item_id bigint,
    max_rows integer = 20,
    skip_offset integer = 0
)
RETURNS TABLE (
    created_date timestamp with time zone,
    created_by text,
    note text
) AS $$
BEGIN
RETURN QUERY 
    SELECT 
        ih.created_date
       ,coalesce(ih.created_by, '(system)') as created_by
       ,ih.note
    FROM
        {schema}.item_history as ih 
        left join {schema}.user us 
        on ih.created_by = us.email
    WHERE
        ih.item_id = history_item_id
    ORDER BY 
        created_date DESC
    LIMIT (max_rows)
    OFFSET (skip_offset);

END;
$$ LANGUAGE plpgsql;

;
ALTER FUNCTION {schema}.item_history_get(bigint, integer, integer)
    OWNER TO postgres;