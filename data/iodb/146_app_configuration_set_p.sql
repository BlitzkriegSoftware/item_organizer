DROP PROCEDURE IF EXISTS {schema}.app_configuration_set;

CREATE OR REPLACE PROCEDURE {schema}.app_configuration_set(
        item_name text,
        new_value text
)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    flag_exists boolean;
BEGIN
    select exists(select setting_name from {schema}.app_configuration0
     where setting_name = item_name ) into flag_exists;
    if flag_exists then
        update {schema}.app_configuration
            set setting_value = new_value
            where setting_name = item_name;
    else
        insert into {schema}.app_configuration(setting_name, setting_value)
            values (item_name, new_value);
    end if;
END;
$BODY$
;

ALTER PROCEDURE {schema}.app_configuration_set(text,text)
    OWNER TO postgres;