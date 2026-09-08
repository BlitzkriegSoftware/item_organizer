DROP FUNCTION IF EXISTS {schema}.app_configuration_get(text);

CREATE or replace FUNCTION {schema}.app_configuration_get
    (
        name text
	) 
RETURNS character varying(128)
 LANGUAGE 'sql'
AS $BODY$
	select setting_value 
    from {schema}.app_configuration 
    where setting_name = name;
$BODY$

;
ALTER FUNCTION {schema}.app_configuration_get(text)
    OWNER TO postgres;
