-- Table: {schema}.item_state

DROP TABLE IF EXISTS {schema}.item_state;

CREATE TABLE IF NOT EXISTS {schema}.item_state
(
    org_id uuid null default '00000000-0000-0000-0000-000000000000',
    item_state_id integer NOT NULL,
    state_title character varying(32),
    PRIMARY KEY (org_id, item_state_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS {schema}.item_state
    OWNER to postgres;