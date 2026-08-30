-- Table: {schema}.user

-- DROP TABLE IF EXISTS {schema}."user";

CREATE TABLE IF NOT EXISTS {schema}."user"
(
    user_id uuid NOT NULL DEFAULT gen_random_uuid(),
    email text COLLATE pg_catalog."default" NOT NULL,
    password_hash text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT user_pkey PRIMARY KEY (user_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS {schema}."user"
    OWNER to postgres;

COMMENT ON TABLE {schema}."user"
    IS 'users';