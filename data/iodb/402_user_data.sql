truncate table {schema}.user;

INSERT INTO {schema}."user"(
	user_id, email, password_hash)
	VALUES ('00000000-0000-0000-0000-000000000000', 
			'admin', 
			'$2b$12$e5A5tg95TlqVjA.7lDDfFutc6PTFsVAsIPqAruMZ7ju.HHf0qVP6G');

INSERT INTO {schema}."user"(
	user_id, email, password_hash)
	VALUES ('00000000-0000-0000-0000-000000000001', 
			'spookdejur@hotmail.com', 
			'$2b$12$e5A5tg95TlqVjA.7lDDfFutc6PTFsVAsIPqAruMZ7ju.HHf0qVP6G');
