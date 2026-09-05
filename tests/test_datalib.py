import pytest
from faker import Faker

from data_lib.datalib import datalib


class test_datalib:
    NO_TEST = "Unable to integration test to postgres"
    test_row_count: int = 3
    schema = "public"
    table = "test_users"
    cols = [
        "id SERIAL PRIMARY KEY,",
        "email VARCHAR(100) NOT NULL,",
        "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    ]
    can_test: bool = False

    def __init__(self) -> None:
        test_datalib.can_test = datalib.connection_ok()

    def test_open_close(self):
        if not test_datalib.can_test:
            pytest.skip(test_datalib.NO_TEST)
            return

        conn = datalib.connection_make()
        assert conn is not None
        datalib.connection_close(conn)
        return

    def test_query_dict(self):
        if not test_datalib.can_test:
            pytest.skip(test_datalib.NO_TEST)
            return

        conn = None
        try:
            conn = datalib.connection_make()
            assert conn is not None

            result = datalib.table_drop(conn, test_datalib.table, test_datalib.schema)
            if not result:
                pytest.fail("Unable to drop test table")

            result = datalib.table_create(
                conn, test_datalib.table, test_datalib.cols, test_datalib.schema
            )
            if not result:
                pytest.fail("Unable to create test table")

            fake = Faker()
            for i in range(test_datalib.test_row_count):
                email = fake.email()
                query = f"insert into {test_datalib.schema}.{test_datalib.table} (email) values ({email});"
                result = datalib.query_execute(conn, query)
                if not result:
                    pytest.fail(f"unable to: {query}")

            query = f"SELECT * FROM {test_datalib.schema}.{test_datalib.table};"
            d = datalib.query_return_dict(conn, query)
            assert d is not None
            print(d)

            result = datalib.table_drop(conn, test_datalib.table, test_datalib.schema)
            if not result:
                pytest.fail("Unable to drop test table")

        finally:
            datalib.connection_close(conn)

        return
