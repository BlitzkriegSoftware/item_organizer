-- Table: {schema}.app_configuration
DROP TABLE IF EXISTS {schema}.app_configuration;

CREATE TABLE {schema}.app_configuration
(
    setting_name text NOT NULL,
    setting_value text NOT NULL,
    unit text DEFAULT 'minutes',
    casted_as text DEFAULT 'integer',
    modified_by text DEFAULT 'system',
    modified_on timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    notes text,
    PRIMARY KEY (setting_name)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS {schema}.app_configuration
    OWNER to postgres;