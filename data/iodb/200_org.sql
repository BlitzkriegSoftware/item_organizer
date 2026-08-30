-- Table: {schema}.organization

-- DROP TABLE IF EXISTS {schema}.organization;

CREATE TABLE IF NOT EXISTS {schema}.organization
(
    org_id uuid NOT NULL DEFAULT gen_random_uuid(),
    parent_org_id uuid default '00000000-0000-0000-0000-000000000000',
    name text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT organization_pkey PRIMARY KEY (org_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS {schema}.organization
    OWNER to postgres;

COMMENT ON TABLE {schema}.organization
    IS 'table of organizations';