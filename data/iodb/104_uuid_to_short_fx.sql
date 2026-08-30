CREATE OR REPLACE FUNCTION {schema}.uuid_to_short(u uuid) 
RETURNS text AS $$
  SELECT translate(
    encode(decode(replace(u::text, '-', ''), 'hex'), 'base64'),
    '+/=', '-_'
  );
$$ LANGUAGE sql IMMUTABLE STRICT;

;
ALTER FUNCTION {schema}.uuid_to_short(uuid)
    OWNER TO postgres;