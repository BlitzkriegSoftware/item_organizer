truncate table {schema}.user_org;

-- Super user
INSERT INTO {schema}.user_org(
	user_id, org_id, org_role_id)
	VALUES ('00000000-0000-0000-0000-000000000000', 
            '00000000-0000-0000-0000-000000000000', 
           16);
            
-- 2nd user
INSERT INTO {schema}.user_org(
	user_id, org_id, org_role_id)
	VALUES ('00000000-0000-0000-0000-000000000001', 
            '00000000-0000-0000-0000-000000000001', 
            8);