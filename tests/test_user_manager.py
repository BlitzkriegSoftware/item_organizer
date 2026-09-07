import os
import pytest

from biz_logic.user_manager import UserManager
from biz_logic.user_status import UserStatus
from data_lib.datalib import DataLib


def test_login():
    IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")
    if not IOR_SCHEMA:
        pytest.fail("IOR_SCHEMA missing")

    email = "admin"
    password = "password123-"

    try:
        UserManager.login(email, password)
    except Exception as ex:
        pytest.fail(str(ex))


def test_make_user():
    IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")
    if not IOR_SCHEMA:
        pytest.fail("IOR_SCHEMA missing")

    email = "test-123@test.tst"
    fullname = "test 123"
    iconurl = ""

    try:
        UserManager.add_user(email, fullname, iconurl)
    except Exception as ex:
        pytest.fail(str(ex))

    try:
        query = f"delete from {IOR_SCHEMA}.user where email = '{email}';"
        DataLib.query_execute_in_one(query)
    except Exception as ex:
        pytest.fail(str(ex))


def test_password_reset_hash_round_trip():
    email = "test-123@test.tst"
    hashed = UserManager.generate_reset_hash(email)
    UserManager.validate_reset_hash(email, hashed)


def test_make_disable_user():
    IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")
    if not IOR_SCHEMA:
        pytest.fail("IOR_SCHEMA missing")

    email = "test-de3@test.tst"
    fullname = "test 123"
    iconurl = ""

    query = f"delete from {IOR_SCHEMA}.user where email = '{email}';"
    DataLib.query_execute_in_one(query)
    if not query:
        pytest.fail("Unable to cleanup")

    try:
        UserManager.add_user(email, fullname, iconurl)
    except Exception as ex:
        pytest.fail(str(ex))

    try:
        status = UserManager.user_status(email)
        if status != UserStatus.CONFIRM:
            pytest.fail(f"Should be {UserStatus.DISABLED} was {status}")
    except Exception as ex:
        pytest.fail(str(ex))

    try:
        UserManager.disable_user(email)
    except Exception as ex:
        pytest.fail(str(ex))

    try:
        status = UserManager.user_status(email)
        if status != UserStatus.DISABLED:
            pytest.fail(f"Should be {UserStatus.DISABLED} was {status}")
    except Exception as ex:
        pytest.fail(str(ex))

    try:
        query = f"delete from {IOR_SCHEMA}.user where email = '{email}';"
        DataLib.query_execute_in_one(query)
    except Exception as ex:
        pytest.fail(str(ex))
