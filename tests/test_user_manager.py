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


def test_password_hash_bad():
    email = "test-123@test.tst"
    hashed = "gorkybot"
    try:
        UserManager.validate_reset_hash(email, hashed)
        pytest.fail("This should fail!")
    except Exception as ex:
        print("pass: ", str(ex))


def test_is_a_user():
    IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")
    if not IOR_SCHEMA:
        pytest.fail("IOR_SCHEMA missing")

    email = DataLib.query_return_single_value_in_one(
        "select email from myio.user order by user_id DESC limit 1;"
    )

    try:
        status = UserManager.user_status(email)
        if status != UserStatus.ACTIVE:
            pytest.fail(f"Should be {UserStatus.ACTIVE} was {status}")
    except Exception as ex:
        pytest.fail(str(ex))


def test_not_a_user():
    IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")
    if not IOR_SCHEMA:
        pytest.fail("IOR_SCHEMA missing")

    email = "gotrder@not-auser.boz"
    UserManager.user_remove_last_resort(email)

    try:
        status = UserManager.user_status(email)
        if status != UserStatus.NOTUSER:
            pytest.fail(f"Should be {UserStatus.NOTUSER} was {status}")
    except Exception as ex:
        pytest.fail(str(ex))


def test_make_disable_user():
    IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")
    if not IOR_SCHEMA:
        pytest.fail("IOR_SCHEMA missing")

    email = "test-de3@test.tst"
    fullname = "test 123"
    iconurl = ""

    UserManager.user_remove_last_resort(email)

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
        UserManager.user_remove_last_resort(email)
    except Exception as ex:
        pytest.fail(str(ex))


def test_user_org_role_get():
    IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")
    if not IOR_SCHEMA:
        pytest.fail("IOR_SCHEMA missing")

    email = DataLib.query_return_single_value_in_one(
        f"select email from {IOR_SCHEMA}.user order by user_id DESC limit 1;"
    )

    org_id = DataLib.query_return_single_value_in_one(
        f"select org_id from {IOR_SCHEMA}.organization order by org_id DESC limit 1;"
    )

    expected = 8
    UserManager.user_org_add_by_email(email, org_id, expected)

    actual = UserManager.user_org_role_get_by_email(email, org_id)
    assert expected == actual

    UserManager.user_org_remove_by_email(email, org_id)


def test_user_org_role_get_bad():
    email = DataLib.query_return_single_value_in_one(
        "select email from myio.user order by user_id DESC limit 1;"
    )

    org_id = DataLib.query_return_single_value_in_one(
        "select org_id from myio.organization order by org_id DESC limit 1;"
    )

    expected = 3
    try:
        UserManager.user_org_add_by_email(email, org_id, expected)
        pytest.fail(f"Not a valid role_id: {expected}")
    except Exception as ex:
        print("success:", ex)
