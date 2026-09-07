DROP PROCEDURE IF EXISTS {schema}.app_configuration_set;

CREATE OR REPLACE PROCEDURE {schema}.app_configuration_set(
        name text,
        new_value text
)
 LANGUAGE 'sql'
AS $BODY$
	update {setting}.app_configuration 
    set setting_value = new_value
    where setting_name = name
    ON CONFLICT (setting_name) 
    DO UPDATE SET setting_value = EXCLUDED.setting_value;
$BODY$

ALTER PROCEDURE {schema}.app_configuration_set(text,text)
    OWNER TO postgres;