-- Table: {schema}.organization

DROP TABLE IF EXISTS {schema}.organization;

CREATE TABLE IF NOT EXISTS {schema}.organization
(
    org_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    parent_org_id BIGINT default 0,
    name text COLLATE pg_catalog."default" NOT NULL
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS {schema}.organization
    OWNER to postgres;

COMMENT ON TABLE {schema}.organization
    IS 'table of organizations';
