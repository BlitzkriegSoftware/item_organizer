-- Table: {schema}.org_role

DROP TABLE IF EXISTS {schema}.org_role;

CREATE TABLE IF NOT EXISTS {schema}.org_role
(
    org_role_id integer NOT NULL DEFAULT 0,
    role_title text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT org_role_pkey PRIMARY KEY (org_role_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS {schema}.org_role
    OWNER to postgres;

COMMENT ON TABLE {schema}.org_role
    IS 'Organization Roles (powers of two)';