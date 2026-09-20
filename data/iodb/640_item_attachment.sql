DROP TABLE IF EXISTS {schema}.item_attachment;

CREATE TABLE IF NOT EXISTS {schema}.item_attachment
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    item_id bigint NOT NULL,
    created_by bigint DEFAULT 0,
    caption text COLLATE pg_catalog."default" NOT NULL,
    storage_url text COLLATE pg_catalog."default" NOT NULL,
    created_date timestamp with time zone DEFAULT now(),
    CONSTRAINT fk_{schema}_item_attachment_item_id FOREIGN KEY (item_id)
        REFERENCES {schema}.item (item_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_{schema}_item_attachment_created_by FOREIGN KEY (created_by)
        REFERENCES {schema}."user" (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS {schema}.item_attachment
    OWNER to postgres;

COMMENT ON TABLE {schema}.item_attachment
    IS 'item attachments';
