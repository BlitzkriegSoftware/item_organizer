truncate table {schema}.user_org;

-- Super user
INSERT INTO {schema}.user_org(
	user_id, org_id, org_role_id)
	VALUES (0, 
            0, 
           16);
            
-- 2nd user
INSERT INTO {schema}.user_org(
	user_id, org_id, org_role_id)
	VALUES (1, 
            1, 
            8);