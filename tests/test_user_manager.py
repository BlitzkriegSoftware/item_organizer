import pytest

from biz_logic.user_manager import UserManager


def test_login():
    email = "admin"
    password = "password123-"

    try:
        UserManager.login(email, password)
    except Exception as ex:
        pytest.fail(str(ex))
