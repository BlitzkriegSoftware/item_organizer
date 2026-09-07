TRUNCATE TABLE {schema}.app_configuration;

INSERT INTO {schema}.app_configuration(
	setting_name, setting_value, unit, casted_as, notes)
	VALUES ('IOR_SALT','JDJiJDEyJGU1QTV0Zzk1VGxxVmpBLjdsRERmRnU=','unit','text','password salt (default)');

INSERT INTO {schema}.app_configuration(
	setting_name, setting_value, unit, casted_as, notes)
	VALUES ('IOR_FERMAT','dENwNS1GVGdKZUhzdFdCcC1VMGtmNl9ZVTBpZWpWLWlhcHd1dUY1M0R2MD0=','unit','text','crypto key (default)');

