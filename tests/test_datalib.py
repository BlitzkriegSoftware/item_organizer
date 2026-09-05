import pytest
from faker import Faker

from data_lib.datalib import datalib


class TestDataLib:
    NO_TEST = "Unable to integration test to postgres"
    test_row_count: int = 3
    schema = "public"
    table = "test_users"
    cols = [
        "id SERIAL PRIMARY KEY",
        "email VARCHAR(100) NOT NULL",
        "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    ]

    def create_proc_text(self) -> str:
        

    def test_open_close(self):
        can_test = datalib.connection_ok()
        if not can_test:
            pytest.skip(TestDataLib.NO_TEST)
            return

        conn = datalib.connection_make()
        assert conn is not None
        datalib.connection_close(conn)
        return

    def test_query_dict(self):
        can_test = datalib.connection_ok()
        if not can_test:
            pytest.skip(TestDataLib.NO_TEST)
            return

        conn = None
        try:
            conn = datalib.connection_make()
            assert conn is not None

            result = datalib.table_drop(conn, TestDataLib.table, TestDataLib.schema)
            if not result:
                pytest.fail("Unable to drop test table")

            result = datalib.table_create(
                conn, TestDataLib.table, TestDataLib.cols, TestDataLib.schema
            )
            if not result:
                pytest.fail("Unable to create test table")

            fake = Faker()
            for i in range(TestDataLib.test_row_count):
                email = fake.email()
                query = f"insert into {TestDataLib.schema}.{TestDataLib.table} (email) values ('{email}');"
                result = datalib.query_execute(conn, query)
                if not result:
                    pytest.fail(f"unable to: {query}")

            query = f"SELECT * FROM {TestDataLib.schema}.{TestDataLib.table};"
            drows = datalib.query_return_dict(conn, query)
            if drows:
                for r in drows:
                    print(r)
            assert drows is not None

            result = datalib.table_drop(conn, TestDataLib.table, TestDataLib.schema)
            if not result:
                pytest.fail("Unable to drop test table")

        finally:
            datalib.connection_close(conn)

        return
