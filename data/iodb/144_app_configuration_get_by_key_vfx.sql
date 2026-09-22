DROP FUNCTION IF EXISTS {schema}.app_configuration_get_by_key(text);

CREATE or replace FUNCTION {schema}.app_configuration_get_by_key
    (
        name text
	) 
RETURNS character text
 LANGUAGE 'sql'
AS $BODY$
	select setting_value 
    from {schema}.app_configuration 
    where setting_name = name;
$BODY$

;
ALTER FUNCTION {schema}.app_configuration_get_by_key(text)
    OWNER TO postgres;
