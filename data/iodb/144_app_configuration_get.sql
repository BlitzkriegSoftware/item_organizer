CREATE or replace FUNCTION {setting}.app_configuration_get
    (
        name character varying(128)
	) 
RETURNS character varying(128)
 LANGUAGE 'sql'
AS $BODY$
	select setting_value 
    from {setting}.app_configuration 
    where setting_name = name;
$BODY$
