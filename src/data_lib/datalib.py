import os
import psycopg2
from functools import cache
from typing import Any
from psycopg2.extras import RealDictCursor, RealDictRow
from varname import nameof

from app_exceptions.db_exception import DatabaseException
from src.app_logger.applogger import AppLogger


class DataLib:
    """
    Holder class for data library methods
    """

    ENV_VAR_DB: str = "IOR_DB"
    ENV_VAR_USER: str = "POSTGRES_USER"
    ENV_VAR_PASSWORD: str = "PGPASSWORD"
    ENV_VAR_HOST: str = "IOR_HOST"
    ENV_VAR_PORT: str = "IOR_DB_PORT"

    DEFAULT_CONNECTION_TIMEOUT_SECONDS: int = 3

    @cache
    @staticmethod
    def connection_config() -> dict[str, str]:
        """
        Fetches configuration from environment variables

        Returns:
            dict[str, str]: configuration
        """
        config = {}
        config[DataLib.ENV_VAR_DB] = os.getenv(DataLib.ENV_VAR_DB, "postgres")
        config[DataLib.ENV_VAR_USER] = os.getenv(DataLib.ENV_VAR_USER, "postgres")
        config[DataLib.ENV_VAR_PASSWORD] = os.getenv(
            DataLib.ENV_VAR_PASSWORD, "password123-"
        )
        config[DataLib.ENV_VAR_HOST] = os.getenv(DataLib.ENV_VAR_HOST, "localhost")
        config[DataLib.ENV_VAR_PORT] = os.getenv(DataLib.ENV_VAR_PORT, "5432")
        return config

    @cache
    @staticmethod
    def connection_string(connection_timeout: int = DEFAULT_CONNECTION_TIMEOUT_SECONDS):
        config = DataLib.connection_config()
        cs = f"postgresql://{config[DataLib.ENV_VAR_USER]}:{config[DataLib.ENV_VAR_PASSWORD]}@{config[DataLib.ENV_VAR_HOST]}:{config[DataLib.ENV_VAR_PORT]}/{config[DataLib.ENV_VAR_DB]}?connect_timeout={connection_timeout}"
        return cs

    @staticmethod
    def connection_make(
        connect_timeout_seconds: int = DEFAULT_CONNECTION_TIMEOUT_SECONDS,
    ) -> psycopg2.extensions.connection | None:
        """
        For the containers environment variables creates
        a connection to the DATABASE (exclusive of the schema)

        Args:
            connect_timeout_seconds: seconds to allow to connect

        Returns:
            psycopg2.extensions.connection | None: connection
        """
        cs = DataLib.connection_string(connect_timeout_seconds)
        try:
            conn = psycopg2.connect(cs)
            conn.autocommit = False
        except Exception as ex:  # pragma: no cover
            AppLogger.log_exception(
                "open connection",
                ex,
                {},
                logger_name=nameof(DataLib.connection_make),
            )
            conn = None

        return conn

    @staticmethod
    def connection_ok() -> bool:
        conn = DataLib.connection_make(1)
        if conn:
            DataLib.connection_close(conn)
            return True
        else:
            return False

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
            except Exception as ex:  # pragma: no cover
                isOk = False
                AppLogger.log_exception(
                    query,
                    ex,
                    {},
                    logger_name=nameof(DataLib.query_execute),
                )
                if conn:
                    conn.rollback()
            finally:
                cursor.close()

        return isOk

    @staticmethod
    def query_execute_in_one(
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
        conn = DataLib.connection_make(DataLib.DEFAULT_CONNECTION_TIMEOUT_SECONDS)
        if not conn:  # pragma: no cover
            raise DatabaseException("unable to connect", query)

        with conn.cursor() as cursor:
            try:
                cursor.execute(query)
                conn.commit()
            except Exception as ex:  # pragma: no cover
                isOk = False
                AppLogger.log_exception(
                    query,
                    ex,
                    {},
                    logger_name=nameof(DataLib.query_execute_in_one)
                )
                if conn:
                    conn.rollback()
            finally:
                cursor.close()

        DataLib.connection_close(conn)

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
        drows: list[RealDictRow] | None = []
        
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute(query)
                drows = cursor.fetchall()
                conn.commit()
            except Exception as ex:  # pragma: no cover
                conn.rollback()
                AppLogger.log_exception(
                    query,
                    ex,
                    {},
                    logger_name=nameof(DataLib.query_return_dict)
                )
                drows = None
            finally:
                cursor.close()

        return drows

    @staticmethod
    def query_return_dict_in_one(
        query: str,
    ) -> list[RealDictRow] | None:
        """
        Does a query that returns rows, and formats each row
        as a `dict` of column w. values.
        Empty [] if no rows, None on error

        Important: Objects should contain Schema info!

        Args:
            query (str): select query

        Returns:
            list[RealDictRow] | None: list[dict]
        """
        drows: list[RealDictRow] | None = []
        conn = DataLib.connection_make()
        if not conn:  # pragma: no cover
            raise DatabaseException("Connection failed", "")
        try:
            drows = DataLib.query_return_dict(conn, query)
        finally:
            DataLib.connection_close(conn)
        return drows

    @staticmethod
    def query_return_single_value_in_one(
        query: str,
    ) -> Any:
        """
        Does a query that returns rows, and formats each row
        as a `dict` of column w. values.
        Empty [] if no rows, None on error

        Important: Objects should contain Schema info!

        Args:
            query (str): select query

        Returns:
            list[RealDictRow] | None: list[dict]
        """
        drows: list[RealDictRow] | None = []
        conn = DataLib.connection_make()
        if not conn:  # pragma: no cover
            raise DatabaseException("Connection failed", "")
        try:
            drows = DataLib.query_return_dict(conn, query)
        finally:
            DataLib.connection_close(conn)
        return DataLib.first_value(drows)

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
                query = DataLib.stored_procedure_make_query(
                    procedure_name, args, schema
                )
                AppLogger.log_info(
                    query, 
                    AppLogger.make_log_extra(procedure_name=procedure_name, args=args), 
                    logger_name=nameof(DataLib.stored_procedure_execute),
                )
                cursor.execute(query, args)
                conn.commit()
            except Exception as ex:  # pragma: no cover
                isOk = False
                if conn:
                    conn.rollback()
                
                AppLogger.log_exception(
                    query,
                    ex,
                    AppLogger.make_log_extra(procedure_name=procedure_name, args=args), 
                    logger_name=nameof(DataLib.stored_procedure_execute)
                )

            finally:
                cursor.close()

        return isOk

    @staticmethod
    def stored_procedure_execute_all_in_one(
        procedure_name: str,
        args: tuple,
        schema: str = "public",
    ) -> bool:
        """
        Execute a SP with args
        Rollsback on failure

        Args:
            procedure_name (str): stored procedure name w. schema
            args (tuple): args list
            schema (str): schema

        Returns:
            bool: True on success
        """
        isOk: bool = True
        conn = DataLib.connection_make()
        if not conn:  # pragma: no cover
            raise DatabaseException("Unable to open db", procedure_name)
        try:
            isOk = DataLib.stored_procedure_execute(conn, procedure_name, args, schema)
        finally:
            DataLib.connection_close(conn)

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
        query = DataLib.stored_procedure_make_query(procedure_name, args, schema)
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute(query, args)
                drows = cursor.fetchall()
            except Exception as ex:  # pragma: no cover
                AppLogger.log_exception(
                    query,
                    ex,
                    {},
                    logger_name=nameof(DataLib.stored_procedure_query)
                )
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
        result = DataLib.query_return_dict(conn, query)
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
        args = DataLib.stored_procedure_args_list(conn, procedure_name, schema)

        query = f"DROP PROCEDURE IF EXISTS {schema}.{procedure_name}({args});"
        result = DataLib.query_execute(conn, query)
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
        drows = DataLib.query_return_dict(conn, query)
        if not drows:
            return False
        value = DataLib.first_value(drows)
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

        result = DataLib.query_execute(conn, query)
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
        result = DataLib.query_execute(conn, query)
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

    @staticmethod
    def has_rows(drows: list[RealDictRow] | None) -> bool:
        if not drows:
            return False
        if len(drows) > 0:
            return True
        return False
