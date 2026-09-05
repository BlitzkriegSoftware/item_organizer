CREATE OR REPLACE PROCEDURE public.test_procedure_no_return(
    p_name TEXT,
    p_age INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_message TEXT;
    v_years_to_100 INT;
BEGIN
    v_years_to_100 := 100 - p_age;
    v_message := format('%s is %s years old and has %s years until 100.', p_name, p_age, v_years_to_100);

    RAISE NOTICE '%', v_message;
END;
$$;