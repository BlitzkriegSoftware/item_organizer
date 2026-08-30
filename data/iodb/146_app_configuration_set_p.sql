CREATE OR REPLACE PROCEDURE {schema}.app_configuration_set(
        name character varying(128),
        new_value character varying(128)
)
 LANGUAGE 'sql'
AS $BODY$
	update {setting}.app_configuration 
    set setting_value = new_value
    where setting_name = name;
$BODY$