-- Table: {schema}.item_state_fsm

DROP TABLE IF EXISTS {schema}.item_state_fsm;

CREATE TABLE IF NOT EXISTS {schema}.item_state_fsm
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    item_state_from_id integer NOT NULL,
    item_state_to_id integer NOT NULL,
    org_id uuid null default '00000000-0000-0000-0000-000000000000'
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS {schema}.item_state_fsm
    OWNER to postgres;
