-- Table: {schema}.item_nv

DROP TABLE IF EXISTS {schema}.item_nv;

CREATE TABLE IF NOT EXISTS {schema}.item_nv
(
    item_id bigint NOT NULL,
    nv_key text COLLATE pg_catalog."default" NOT NULL,
    nv_value text COLLATE pg_catalog."default" NOT NULL,
    search_vector tsvector GENERATED ALWAYS AS (
         setweight(to_tsvector('english', COALESCE(nv_key, '')), 'A'::"char") || 
         setweight(to_tsvector('english', COALESCE(nv_value)), 'B'::"char") || 
         setweight(to_tsvector('simple', item_id::text), 'C'::"char")
    ) STORED,
    CONSTRAINT item_nv_pkey PRIMARY KEY (item_id, nv_key),
    CONSTRAINT fk_{schema}_item_nv_item_id FOREIGN KEY (item_id)
        REFERENCES {schema}.item (item_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS {schema}.item_nv
    OWNER to postgres;

COMMENT ON TABLE {schema}.item_nv
    IS 'item name value pairs (extension data)';
