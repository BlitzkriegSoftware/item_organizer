from typing import Any
import psycopg2
from psycopg2.extras import RealDictCursor, RealDictRow
import os
from src.applogger.applogger import configure_logging


class datalib:
    """
    Holder class for data library methods
    """

    @staticmethod
    def connection_ok() -> bool:
        conn = datalib.connection_make(1)
        if conn:
            datalib.connection_close(conn)
            return True
        else:
            return False

    @staticmethod
    def connection_make(
        connect_timeout_seconds: int = 3,
    ) -> psycopg2.extensions.connection | None:
        """
        For the containers environment variables creates
        a connection to the DATABASE (exclusive of the schema)

        Args:
            connect_timeout_seconds: seconds to allow to connect

        Returns:
            psycopg2.extensions.connection | None: connection
        """
        ior_db = os.getenv("IOR_DB", "postgres")
        postgres_user = os.getenv("POSTGRES_USER", "postgres")
        pgpass = os.getenv("PGPASSWORD", "password123-")
        ior_host = "localhost"
        ior_port = os.getenv("IOR_PORT", "5432")

        try:
            conn = psycopg2.connect(
                dbname=ior_db,
                user=postgres_user,
                password=pgpass,
                host=ior_host,
                port=ior_port,
                connect_timeout=connect_timeout_seconds,
            )
            conn.autocommit = False
        except Exception:  # pragma: no cover
            logger = configure_logging()
            logger.exception("make: %s,%s", ior_db, postgres_user)
            conn = None

        return conn

    @staticmethod
    def connection_close(conn: psycopg2.extensions.connection | None):
        """
        Safely close a connection
        Sets it to None

        Args:
            conn (psycopg2.extensions.connection | None): connection
        """
        if conn:
            conn.close()

        conn = None

    @staticmethod
    def query_execute(
        conn: psycopg2.extensions.connection,
        query: str,
    ) -> bool:
        """
        Execute a query that returns no rows returns true if no errors
        false if not, and does a rollback!

        Important: Objects should contain Schema info!

        Args:
            conn (psycopg2.extensions.connection): connection
            query (str): query with must be a valid SQL

        Returns:
            bool: True on success
        """
        isOk: bool = True
        with conn.cursor() as cursor:
            try:
                cursor.execute(query)
                conn.commit()
            except Exception:  # pragma: no cover
                isOk = False
                logger = configure_logging()
                logger.exception("query: %s", query)
                if conn:
                    conn.rollback()
            finally:
                cursor.close()

        return isOk

    @staticmethod
    def query_return_dict(
        conn: psycopg2.extensions.connection,
        query: str,
    ) -> list[RealDictRow] | None:
        """
        Does a query that returns rows, and formats each row
        as a `dict` of column w. values.
        Empty [] if no rows, None on error

        Important: Objects should contain Schema info!

        Args:
            conn (psycopg2.extensions.connection): connection
            query (str): select query

        Returns:
            list[RealDictRow] | None: list[dict]
        """
        drows: list[RealDictRow] | None
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute(query)
                drows = cursor.fetchall()
            except Exception:  # pragma: no cover
                logger = configure_logging()
                logger.exception("query: %s", query)
                drows = None
            finally:
                cursor.close()

        return drows

    @staticmethod
    def stored_procedure_make_query(
        procedure_name: str,
        args: tuple,
        schema: str,
    ) -> str:
        """
        Makes a well formed CALL

        Args:
            procedure_name (str): sp name
            args (tuple): args tuple
            schema (str): schema

        Returns:
            str: query part
        """
        query: str = ""
        query += f"CALL {schema}.{procedure_name}("
        for i in range(len(args)):
            query += "%s, "
        query = query.strip()
        if query.endswith(","):
            query = query[:-1]
        query += ");"
        return query

    @staticmethod
    def stored_procedure_execute(
        conn: psycopg2.extensions.connection,
        procedure_name: str,
        args: tuple,
        schema: str = "public",
    ) -> bool:
        """
        Execute a SP with args
        Rollsback on failure

        Args:
            conn (psycopg2.extensions.connection): connection
            procedure_name (str): stored procedure name w. schema
            args (tuple): args list
            schema (str): schema

        Returns:
            bool: True on success
        """
        isOk: bool = True
        query: str = ""
        with conn.cursor() as cursor:
            try:
                query = datalib.stored_procedure_make_query(
                    procedure_name, args, schema
                )
                cursor.execute(query, args)
                conn.commit()
            except Exception:  # pragma: no cover
                isOk = False
                logger = configure_logging()
                logger.exception("query: %s(%s)", query, args)
                if conn:
                    conn.rollback()
            finally:
                cursor.close()

        return isOk

    @staticmethod
    def stored_procedure_query(
        conn: psycopg2.extensions.connection,
        procedure_name: str,
        args: tuple,
        schema: str,
    ):
        """
        execute stored procedure returning rows

        Args:
            conn (psycopg2.extensions.connection): connection
            procedure_name (str): stored procedure name
            args (tuple): args list
            schema (str): schema

        Returns:
            list[dict], empty if no matches, None on error
        """
        drows: list[RealDictRow] | None
        query = datalib.stored_procedure_make_query(procedure_name, args, schema)
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute(query, args)
                drows = cursor.fetchall()
            except Exception:  # pragma: no cover
                logger = configure_logging()
                logger.exception("query: %s(%s)", procedure_name, args)
                drows = None
            finally:
                cursor.close()

        return drows

    @staticmethod
    def stored_procedure_args_list(
        conn: psycopg2.extensions.connection,
        procedure_name: str,
        schema: str,
    ) -> str | None:
        query = f"""
            SELECT 
                r.routine_schema AS schema_name,
                r.routine_name AS procedure_name,
                p.parameter_name,
                p.data_type,
                p.parameter_mode
            FROM information_schema.routines r
            JOIN information_schema.parameters p 
                ON r.specific_name = p.specific_name 
            AND r.specific_schema = p.specific_schema
            WHERE r.routine_type = 'PROCEDURE'
            AND r.routine_schema = '{schema}'
            AND r.routine_name = '{procedure_name}'
            ORDER BY p.ordinal_position;
        """
        args = ""
        result = datalib.query_return_dict(conn, query)
        if result:
            for row in result:
                dt = row["data_type"]
                args += dt + ", "

            args = args.strip()
            if len(args) > 1:
                args = args[:-1]

        return args

    @staticmethod
    def stored_procedure_drop(
        conn: psycopg2.extensions.connection,
        procedure_name,
        schema: str,
    ) -> bool:
        args = datalib.stored_procedure_args_list(conn, procedure_name, schema)

        query = f"DROP PROCEDURE IF EXISTS {schema}.{procedure_name}({args});"
        result = datalib.query_execute(conn, query)
        if not result:
            return False

        return True

    @staticmethod
    def table_exists(
        conn: psycopg2.extensions.connection,
        table: str,
        schema: str = "public",
    ) -> bool:
        """
        _summary_

        Args:
            conn (psycopg2.extensions.connection): connection
            table (str): table name
            schema (str): schema

        Returns:
            bool: _description_
        """
        query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = '{schema}' AND table_name = '{table}');"
        drows = datalib.query_return_dict(conn, query)
        if not drows:
            return False
        value = datalib.first_value(drows)
        return value

    @staticmethod
    def table_create(
        conn: psycopg2.extensions.connection,
        table: str,
        columns: list[str],
        schema: str = "public",
    ) -> bool:
        """
        Creates a table for testing

        Args:
            conn (psycopg2.extensions.connection): connection
            table (str): table name
            columns (list[str]): array of column definitions
            schema (str): (default: public)

        Returns:
            bool: True on success
        """
        query = f"CREATE TABLE IF NOT EXISTS {schema}.{table} ("
        for c in columns:
            c = c.strip()
            query += c
            if not c.endswith(","):
                query += ","

        query = query.strip()
        query = query[:-1]
        query += " );"

        print(f"{query}")

        result = datalib.query_execute(conn, query)
        if not result:
            return False

        return True

    @staticmethod
    def table_drop(
        conn: psycopg2.extensions.connection,
        table: str,
        schema: str = "public",
    ) -> bool:
        """
        Drop a table if it exists

        Args:
            conn (psycopg2.extensions.connection): connection
            table (str): table name
            schema (str, optional): Defaults to "public".

        Returns:
            bool: True on success
        """
        query = f"DROP TABLE IF EXISTS {schema}.{table};"
        result = datalib.query_execute(conn, query)
        if not result:
            return False

        return True

    @staticmethod
    def first_value(drows: list[RealDictRow] | None) -> Any:
        if not drows:
            return None

        if len(drows) <= 0:
            return None

        first_val = next(iter(drows[0].values()))
        return first_val
