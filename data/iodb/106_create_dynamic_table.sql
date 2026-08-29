/*
To create a table named my_dynamic_table with 5 columns (col_1 through col_5), 
run:

    SELECT create_dynamic_table('my_dynamic_table', 5);
*/
CREATE OR REPLACE FUNCTION {schema}.create_dynamic_table(
    p_table_name TEXT, 
    p_num_columns INT
) 
RETURNS VOID AS $$
DECLARE
    v_sql TEXT;
    i INT;
BEGIN
    -- 1. Initialize the baseline CREATE TABLE statement securely
    v_sql := format('CREATE TABLE %I (id SERIAL PRIMARY KEY', p_table_name);

    -- 2. Loop to append 'n' number of columns dynamically
    FOR i IN 1..p_num_columns LOOP
        v_sql := v_sql || format(', col_%s TEXT null', i);
    END LOOP;

    -- 3. Close the SQL bracket
    v_sql := v_sql || ');';

    RAISE NOTICE 'create_dynamic_table: %s', v_sql;

    -- 4. Execute the constructed SQL string
    EXECUTE v_sql;
END;
$$ LANGUAGE plpgsql;
