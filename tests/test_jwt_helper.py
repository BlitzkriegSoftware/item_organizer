import pytest
import time
from jwt_lib.jwt_helper import JWTHelper


def test_jwt_key_get():
    key = JWTHelper.jwt_key_get()
    print(key)
    assert key is not None
    assert len(key) > 0


@pytest.mark.parametrize(
    "seconds, did_error",
    [
        (1000, False),
        (1, True),
    ],
)
def test_jwt_round_trip(seconds: int, did_error: bool):
    token = ""
    exploded = False
    d: dict[str, str] = {"abc": "def", "ghi": "jkl"}

    try:
        exp = JWTHelper.seconds_from_now(seconds)
        token = JWTHelper.create_access_token(d, exp)
        assert token is not None
        print(token)
    except Exception as ex:
        exploded = True
        print(ex)

    if did_error:
        time.sleep(seconds * 1.5)

    if not exploded:
        try:
            nd = JWTHelper.validate_token(token)
            print(nd)
        except Exception as ex:
            exploded = True
            print(ex)

    assert exploded == did_error
