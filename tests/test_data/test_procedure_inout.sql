CREATE OR REPLACE PROCEDURE public.test_procedure_inout(
    p_name TEXT,
    p_age INT,
    INOUT p_result TEXT DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    p_result := format('%s is %s years old.', p_name, p_age);
END;
$$;