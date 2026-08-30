CREATE OR REPLACE FUNCTION {schema}.is_org_or_descendant(
    p_org_id uuid,
    p_ancestor_org_id uuid
)
RETURNS boolean
LANGUAGE sql
STABLE
AS $$
    WITH RECURSIVE org_chain AS (
        -- anchor: the org in question
        SELECT org_id, parent_org_id
        FROM {schema}.organization
        WHERE org_id = p_org_id

        UNION ALL

        -- walk up to the parent, but stop once we've reached a self-referencing root
        SELECT o.org_id, o.parent_org_id
        FROM {schema}.organization o
        JOIN org_chain oc ON o.org_id = oc.parent_org_id
        WHERE oc.org_id <> oc.parent_org_id
    )
    SELECT EXISTS (
        SELECT 1
        FROM org_chain
        WHERE org_id = p_ancestor_org_id
    );
$$;