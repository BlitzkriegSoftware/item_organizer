DROP TABLE IF EXISTS {schema}.item_relation;

CREATE TABLE IF NOT EXISTS {schema}.item_relation
(
    from_item_id bigint NOT NULL,
    to_item_id bigint NOT NULL,
    relationship_id integer NOT NULL,
    CONSTRAINT item_relation_pkey PRIMARY KEY (from_item_id, to_item_id),
    CONSTRAINT fk_{schema}_item_relation_from_item_id FOREIGN KEY (from_item_id)
        REFERENCES {schema}.item (item_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_{schema}_item_relation_to_item_id FOREIGN KEY (to_item_id)
        REFERENCES {schema}.item (item_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_{schema}_item_relation_relationship_id FOREIGN KEY (relationship_id)
        REFERENCES {schema}.relationship (relationship_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS {schema}.item_relation
    OWNER to postgres;

COMMENT ON TABLE {schema}.item_relation
    IS 'relation between items';
