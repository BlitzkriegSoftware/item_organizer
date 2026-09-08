-- Table: {schema}.user_org

DROP TABLE IF EXISTS {schema}.user_org;

CREATE TABLE IF NOT EXISTS {schema}.user_org
(
    org_id bigint NOT NULL,
    user_id bigint NOT NULL,
    org_role_id integer NOT NULL DEFAULT 2,
    CONSTRAINT user_org_pkey PRIMARY KEY (user_id, org_id),
    CONSTRAINT fk_{schema}_user_org_org_id FOREIGN KEY (org_id)
        REFERENCES {schema}.organization (org_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_{schema}_user_org_user_id FOREIGN KEY (user_id)
        REFERENCES {schema}.user (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_{schema}_user_org_org_role_id FOREIGN KEY (org_role_id)
        REFERENCES {schema}.org_role (org_role_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS {schema}.user_org
    OWNER to postgres;

COMMENT ON TABLE {schema}.user_org
    IS 'user to organization mapping with role';