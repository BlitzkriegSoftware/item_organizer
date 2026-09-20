DROP FUNCTION IF EXISTS {schema}.item_relation_get(bigint);

CREATE or replace FUNCTION {schema}.item_relation_get(
    desired_item_id bigint
) 
RETURNS TABLE (
    from_id integer,
    to_id integer,
    re_id integer,
    cap_text text
) AS $$
BEGIN
RETURN QUERY 
    SELECT
        ir.from_item_id,
        ir.to_item_id,
        ir.relationship_id,
        re.caption
    FROM {schema}.item_relation ir 
    LEFT JOIN {schema}.relationship re  
    on ir.relationship_id = re.relationship_id
    WHERE
        ir.from_item_id = desired_item_id
    ORDER BY
        re.relationship_id DESC
    ;
END;
$$ LANGUAGE plpgsql;

;
ALTER FUNCTION {schema}.item_relation_get(bigint)
    OWNER TO postgres;