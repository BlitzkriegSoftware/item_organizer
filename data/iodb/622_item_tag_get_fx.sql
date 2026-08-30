CREATE or replace FUNCTION {schema}.item_tag_get(
    desired_item_id bigint
) 
RETURNS TABLE (
    tag text
) AS $$
BEGIN
RETURN QUERY 
    SELECT 
       it.tag
    FROM
        {schema}.item_tag it
    WHERE
        it.item_id = desired_item_id
    ORDER BY 
        it.tag ASC
    ;
END;
$$ LANGUAGE plpgsql;

;
ALTER FUNCTION {schema}.item_tag_get(bigint)
    OWNER TO postgres;