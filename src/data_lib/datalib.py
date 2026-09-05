import psycopg2
import os
import logging

logger = logging.getLogger(__name__)


@staticmethod
def connection_make() -> psycopg2.extensions.connection | None:
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
        )
        conn.autocommit = False
    except Exception:
        logger.exception("connection_make: %s,%s", ior_db, postgres_user)
        conn = None

    return conn


@staticmethod
def connection_close(conn: psycopg2.extensions.connection | None):
    if conn:
        conn.close()


@staticmethod
def execute_query(
    conn: psycopg2.extensions.connection,
    query: str,
) -> bool:
    isOk: bool = True
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
    except Exception:
        isOk = False
        logger.exception("execute_query: %s", query)
        if conn:
            conn.rollback()  # Roll back changes if something goes wrong
    finally:
        cursor.close()

    return isOk
