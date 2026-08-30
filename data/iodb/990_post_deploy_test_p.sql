CREATE OR REPLACE PROCEDURE {schema}.post_deploy_test(
    -- 0 clear no data, 1 at begining, 2 at begining and end of test
    test_flag integer DEFAULT 2,
    -- How many iterations
    test_iterations integer DEFAULT 10
)
LANGUAGE 'plpgsql'
AS $BODY$

DECLARE
    I integer = 0;
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
    test_result INTEGER DEFAULT 0; -- 0 Pass, 1 Fail
    test_result_text text = '';

BEGIN 

    IF test_flag > 0 THEN
        call {schema}.reset_backlog();
        RAISE NOTICE 'reset_backlog';
    END IF;

    FOR I IN 1..test_iterations LOOP

        -- TBD

    END LOOP;

    IF test_flag > 1 THEN
        call {schema}.reset_backlog();
        RAISE NOTICE 'reset_backlog';
    END IF;

    -- Test Results
    IF test_result = 0 THEN
        test_result_text := 'pass';
    ELSE
        test_result_text := 'fail';
    END IF;

	RAISE NOTICE 'test result: %, Failed Tests: %', test_result_text, test_bad;

END;
$BODY$;

ALTER PROCEDURE {schema}.post_deploy_test(integer, integer)
    OWNER TO postgres;
