truncate table {schema}.user;

INSERT INTO {schema}."user"(
	user_id, email, password_hash)
	OVERRIDING SYSTEM VALUE 
	VALUES (0, 
			'admin', 
			'$2b$12$e5A5tg95TlqVjA.7lDDfFutc6PTFsVAsIPqAruMZ7ju.HHf0qVP6G');

INSERT INTO {schema}."user"(
	user_id, email, password_hash)
	OVERRIDING SYSTEM VALUE 
	VALUES (1, 
			'spookdejur@hotmail.com', 
			'$2b$12$e5A5tg95TlqVjA.7lDDfFutc6PTFsVAsIPqAruMZ7ju.HHf0qVP6G');
