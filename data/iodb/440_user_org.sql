-- Table: {schema}.user_org

DROP TABLE IF EXISTS {schema}.user_org;

CREATE TABLE IF NOT EXISTS {schema}.user_org
(
    user_id uuid NOT NULL,
    org_id uuid NOT NULL,
    org_role_id integer NOT NULL DEFAULT 2,
    CONSTRAINT user_org_pkey PRIMARY KEY (user_id, org_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS {schema}.user_org
    OWNER to postgres;

COMMENT ON TABLE {schema}.user_org
    IS 'user to organization mapping';