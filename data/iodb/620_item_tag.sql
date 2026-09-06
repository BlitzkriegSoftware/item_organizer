-- Table: {schema}.item_tag

DROP TABLE IF EXISTS {schema}.item_tag;

CREATE TABLE IF NOT EXISTS {schema}.item_tag
(
    item_id bigint NOT NULL,
    tag text COLLATE pg_catalog."default" NOT NULL,
    search_vector tsvector GENERATED ALWAYS AS (
         setweight(to_tsvector('english', COALESCE(tag, '')), 'A'::"char") || 
         setweight(to_tsvector('simple', item_id::text), 'B'::"char")
    ) STORED,
    CONSTRAINT item_tag_pkey PRIMARY KEY (item_id, tag),
    CONSTRAINT fk_{schema}_item_tag_item_id FOREIGN KEY (item_id)
        REFERENCES {schema}.item (item_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS {schema}.item_tag
    OWNER to postgres;

COMMENT ON TABLE {schema}.item_tag
    IS 'item tag cloud';
