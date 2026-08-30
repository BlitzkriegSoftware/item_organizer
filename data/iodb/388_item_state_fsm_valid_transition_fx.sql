CREATE or replace FUNCTION {schema}.item_state_fsm_valid_transition(
    from_state integer,
    to_state integer,
    desired_org_id uuid = '00000000-0000-0000-0000-000000000000'
) 
RETURNS boolean
LANGUAGE sql
STABLE
AS $$
    SELECT EXISTS (
        select 1
        from {schema}.item_state_fsm
        where (
            item_state_from_id = from_state and 
            item_state_to_id = to_state and 
            org_id = desired_org_id
        )
    );
$$;