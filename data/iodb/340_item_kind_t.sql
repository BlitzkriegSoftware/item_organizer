DROP TABLE IF EXISTS {schema}.item_kind;

CREATE TABLE IF NOT EXISTS {schema}.item_kind
(
    item_kind_id integer NOT NULL,
    kind_title text COLLATE pg_catalog."default" NOT NULL,
    notes text null,
    CONSTRAINT priority_pkey PRIMARY KEY (item_kind_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS {schema}.item_kind
    OWNER to postgres;

COMMENT ON TABLE {schema}.item_kind
    IS 'Item Kind';
