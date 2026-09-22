DROP TABLE IF EXISTS {schema}.relationship;

CREATE TABLE IF NOT EXISTS {schema}.relationship
(
    relationship_id integer NOT NULL,
    reciprocal_relationship_id integer NOT NULL,
    relationship_title text COLLATE pg_catalog."default" NOT NULL,
    notes text null,
    CONSTRAINT relationship_pkey PRIMARY KEY (relationship_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS {schema}.relationship
    OWNER to postgres;

COMMENT ON TABLE {schema}.relationship
    IS 'Relation between items';
