import pytest
from common_helpers.base64_helpers import Base64Helper


def test_base64_h():
    text = "the quick brown fox jumped over the lazy dog."
    b64 = Base64Helper.to_base64_s(text)
    if not b64:
        pytest.fail("b64 cvrt")
    result = Base64Helper.is_base64(b64)
    if not result:
        pytest.fail("Not b64")
    text2 = Base64Helper.from_base64_s(b64)
    assert text == text2


def test_not_base64():
    text = "the quick brown fox jumped over the lazy dog."
    result = Base64Helper.is_base64(text)
    if result:
        pytest.fail("Not b64")
