CREATE or replace FUNCTION {schema}.user_org_role_get(
    current_user_id uuid,
    target_org_id uuid
)
returns integer
LANGUAGE plpgsql
AS $$

DECLARE
  role_id integer := 0;
  try_it bool := true;
  empty_uuid uuid := '00000000-0000-0000-0000-000000000000';
  try_org_id uuid := '00000000-0000-0000-0000-000000000000';
  head_org_id uuid := '00000000-0000-0000-0000-000000000000';

BEGIN

    select COALESCE(uo.org_role_id, -1) into role_id
    from {schema}.user_org uo 
    where (
        uo.user_id = current_user_id and 
        uo.org_id = target_org_id
    );

    IF role_id >= 0 THEN
        RETURN role_id;
    END IF;

    -- no? climb up until we find a role, or fall off.
    try_org_id := target_org_id;
    WHILE (try_it) LOOP

        head_org_id := null;
        SELECT parent_org_id into head_org_id
        FROM {schema}.organization
        where org_id = try_org_id;

        IF head_org_id is null THEN
            try_it := false;
            role_id := -1;
        ELSE
            role_id = -1;
            select COALESCE(uo.org_role_id, -1) into role_id
            from {schema}.user_org uo 
            where (
                uo.user_id = current_user_id and 
                uo.org_id = head_org_id
            );
            IF role_id >= 0 OR head_org_id = empty_uuid THEN
                try_it = false;
            END IF;
        END IF; 

    END LOOP;

    if role_id is null THEN
        role_id := -1;
    end if;
    
    RETURN role_id;
END;
$$;

 ;
ALTER FUNCTION {schema}.user_org_role_get(uuid,uuid)
    OWNER TO postgres;