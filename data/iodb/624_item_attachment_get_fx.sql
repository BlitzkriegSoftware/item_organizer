DROP FUNCTION IF EXISTS {schema}.item_attachment_get(bigint);

-- using inline sql, not working as expected w.  psycopg2.extras import RealDictRow

-- CREATE or replace FUNCTION {schema}.item_attachment_get(
--     desired_item_id bigint
-- ) 
-- RETURNS TABLE (
--     created_by bigint,
--     email text,
--     caption text,
--     storage_url text,
--     created_date timestamp with time zone
-- ) AS $$
-- BEGIN
-- RETURN QUERY 
--     SELECT 
--        ia.created_by,
--        ur.email,
--        ia.caption,
--        ia.storage_url,
--        ia.created_date
--     FROM
--         {schema}.item_attachment ia
--         left join {schema}.user ur 
--         on ia.created_by = ur.user_id
--     WHERE
--         ia.item_id = desired_item_id
--     ORDER BY 
--         ia.created_date DESC
--     ;
-- END;
-- $$ LANGUAGE plpgsql;

-- ;
-- ALTER FUNCTION {schema}.item_attachment_get(bigint)
--     OWNER TO postgres;