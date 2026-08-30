-- Table: {schema}.item

DROP TABLE IF EXISTS {schema}.item_history;

CREATE TABLE IF NOT EXISTS {schema}.item_history
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    item_id bigint NOT NULL,
    created_date timestamp with time zone DEFAULT now(),
    created_by uuid NULL DEFAULT '00000000-0000-0000-0000-000000000000',
    note text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT item_history_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS {schema}.item_history
    OWNER to postgres;

COMMENT ON TABLE {schema}.item_history
    IS 'item history';