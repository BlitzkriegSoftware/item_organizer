-- Table: {schema}.priority

DROP TABLE IF EXISTS {schema}.priority;

CREATE TABLE IF NOT EXISTS {schema}.priority
(
    priority_id integer NOT NULL,
    priority_title text COLLATE pg_catalog."default" NOT NULL,
    notes text null,
    CONSTRAINT priority_pkey PRIMARY KEY (priority_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS {schema}.priority
    OWNER to postgres;
