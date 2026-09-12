DROP FUNCTION IF EXISTS {schema}.item_nv_get(bigint);

CREATE or replace FUNCTION {schema}.item_nv_get(
    desired_item_id bigint
) 
RETURNS TABLE (
    nv_key text,
    nv_value text
) AS $$
BEGIN
RETURN QUERY 
    SELECT 
       it.nv_key
      ,it.nv_value
    FROM
        {schema}.item_nv it
    WHERE
        it.item_id = desired_item_id
    ORDER BY 
        it.nv_key ASC
    ;
END;
$$ LANGUAGE plpgsql;

;
ALTER FUNCTION {schema}.item_nv_get(bigint)
    OWNER TO postgres;