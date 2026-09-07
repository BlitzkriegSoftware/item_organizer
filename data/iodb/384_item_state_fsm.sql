-- Table: {schema}.item_state_fsm

DROP TABLE IF EXISTS {schema}.item_state_fsm;

CREATE TABLE IF NOT EXISTS {schema}.item_state_fsm
(
    org_id uuid null default '00000000-0000-0000-0000-000000000000',
    item_state_from_id integer NOT NULL,
    item_state_to_id integer NOT NULL,
    PRIMARY KEY(org_id, item_state_from_id, item_state_to_id),
    CONSTRAINT fk_{schema}_item_state_fsm_org FOREIGN KEY (org_id)
        REFERENCES {schema}.organization (org_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_{schema}_item_state_fsm_item_state_from_id FOREIGN KEY (org_id, item_state_from_id)
        REFERENCES {schema}.item_state (org_id, item_state_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_{schema}_item_state_fsm_item_state_to_id FOREIGN KEY (org_id, item_state_to_id)
        REFERENCES {schema}.item_state (org_id, item_state_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS {schema}.item_state_fsm
    OWNER to postgres;
