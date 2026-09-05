import pytest

from data_lib.datalib import datalib


class test_datalib:
    NO_TEST = "Unable to integration test to postgres"
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

        conn = datalib.connection_make()
        assert conn is not None

        query = "SELECT schema_name FROM information_schema.schemata;"

        d = datalib.query_return_dict(conn, query)
        assert d is not None
        print(d)

        datalib.connection_close(conn)
        return
