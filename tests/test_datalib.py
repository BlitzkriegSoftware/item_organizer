from pathlib import Path

import pytest
from faker import Faker

from data_lib.datalib import datalib


@pytest.fixture
def load_asset(request):
    """Fixture to load JSON data files from the current test's directory."""

    def _loader(filename: str):
        # Dynamically targets the folder of the running test file
        test_dir = Path(request.path).parent
        asset_path = test_dir / "test_data" / filename

        if not asset_path.exists():
            raise FileNotFoundError(f"Asset not found at: {asset_path}")

        with open(asset_path, "r", encoding="utf-8") as f:
            return f.read()

    return _loader


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

    # -----------------------------------------

    def test_open_close(self):
        can_test = datalib.connection_ok()
        if not can_test:
            pytest.skip(TestDataLib.NO_TEST)
            return

        conn = datalib.connection_make()
        assert conn is not None
        datalib.connection_close(conn)
        return

    def test_create_procedure_no_return(self, load_asset):
        test_file = "test_procedure_no_return.sql"
        query = load_asset(test_file)
        can_test = datalib.connection_ok()
        if not can_test:
            pytest.skip(TestDataLib.NO_TEST)
            return

        conn = datalib.connection_make()
        assert conn is not None

        result = datalib.query_execute(conn, query)
        if not result:
            pytest.fail(f"unable to create: {test_file}")

        schema = "public"
        proc_name = "test_procedure_no_return"
        args = ("alice", 30)

        print(f">> {proc_name}, {args}")

        result = datalib.stored_procedure_execute(conn, proc_name, args, schema)
        if not result:
            pytest.fail(f"unable to execute: {test_file}({args})")

        result = datalib.stored_procedure_drop(conn, proc_name, schema)
        if not result:
            pytest.fail(f"Could not drop: {proc_name}")

        datalib.connection_close(conn)
        return

    def test_create_procedure_query(self, load_asset):
        test_file = "test_procedure_inout.sql"
        query = load_asset(test_file)
        can_test = datalib.connection_ok()
        if not can_test:
            pytest.skip(TestDataLib.NO_TEST)
            return

        conn = datalib.connection_make()
        assert conn is not None

        result = datalib.query_execute(conn, query)
        if not result:
            pytest.fail(f"unable to create: {test_file}")

        schema = "public"
        proc_name = "test_procedure_inout"
        args = ("alice", 30)

        print(f">> {proc_name}, {args}")

        result = datalib.stored_procedure_query(conn, proc_name, args, schema)
        if not result:
            pytest.fail(f"unable to execute: {test_file}({args})")
        else:
            for row in result:
                print(row)

        result = datalib.stored_procedure_drop(conn, proc_name, schema)
        if not result:
            pytest.fail(f"Could not drop: {proc_name}")

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

            result = datalib.table_exists(conn, TestDataLib.table, TestDataLib.schema)
            if not result:
                pytest.fail("Test table should exist")

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
