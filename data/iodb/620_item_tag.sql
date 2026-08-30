-- Table: {schema}.item_tag

DROP TABLE IF EXISTS {schema}.item_tag;

CREATE TABLE IF NOT EXISTS {schema}.item_tag
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    item_id bigint NOT NULL,
    tag text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT item_tag_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS {schema}.item_tag
    OWNER to postgres;

COMMENT ON TABLE {schema}.item_tag
    IS 'item tag cloud';

-- Indexes
CREATE INDEX idx_{schema}_tag_item_id ON {schema}.item_tag(item_id);

-- FKs
ALTER TABLE {schema}.item_tag 
ADD CONSTRAINT fk_{schema}_item_tag_item_id
FOREIGN KEY (item_id) REFERENCES {schema}.item(item_id);
