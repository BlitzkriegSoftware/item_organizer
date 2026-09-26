import string
import pytest

from common_helpers.random_helpers import RandomHelper
from common_helpers.type_validators import TypeValidators


@pytest.mark.parametrize(
    "valid, excluded",
    [
        (string.digits, "iIoO"),
        (string.digits, "iIoO"),
        (string.ascii_letters, "iIoO"),
        (string.ascii_letters, "iIoO"),
        (string.whitespace + string.ascii_letters, "iIoO"),
        (string.printable, "iIoO"),
        (string.ascii_letters, "iIoO"),
        (string.printable, "iIoO"),
    ],
)
def test_random_string(valid: str, excluded: str):
    actual = RandomHelper.random_string(10, valid, excluded)
    trimmed = RandomHelper.remove_from_alphabet(valid, excluded)
    expected = TypeValidators.has_only(actual, trimmed)
    assert expected
