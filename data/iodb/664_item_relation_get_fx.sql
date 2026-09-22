DROP FUNCTION IF EXISTS {schema}.item_relation_get(bigint);


-- using inline sql, not working as expected w.  psycopg2.extras import RealDictRow


-- CREATE or replace FUNCTION {schema}.item_relation_get(
--     desired_item_id bigint
-- ) 
-- RETURNS TABLE (
--     to_id integer,
--     to_title text,
--     re_id integer,
--     re_text text
-- ) AS $$
-- BEGIN
-- RETURN QUERY 
--     SELECT
--         ir.to_item_id,
--         it.title,
--         ir.relationship_id,
--         re.relationship_title
--     FROM {schema}.item_relation ir 
--     LEFT JOIN {schema}.relationship re  
--     on ir.relationship_id = re.relationship_id
--     LEFT JOIN {schema}.Item it 
--     on ir.to_item_id = it.item_it
--     WHERE
--         ir.from_item_id = desired_item_id
--     ORDER BY
--         re.relationship_id DESC
--     ;
-- END;
-- $$ LANGUAGE plpgsql;

-- ;
-- ALTER FUNCTION {schema}.item_relation_get(bigint)
--     OWNER TO postgres;