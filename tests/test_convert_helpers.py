import string
from typing import Any

import pytest

from common_helpers.convert_helpers import ConvertHelpers


@pytest.mark.parametrize(
    "the_value, default_value, expected",
    [
        (1, 0, 1),
        ("one", 1, 1),
        ("cows", 0, 0),
    ],
)
def test_safe_to_int(the_value: Any, default_value: int, expected: int):
    v = ConvertHelpers.safe_to_int(1, 0)
    assert v == 1


@pytest.mark.parametrize(
    "inText, valid, expected",
    [
        ("123", string.digits, "123"),
        ("123saa", string.digits, "123"),
        ("123", string.ascii_letters, ""),
        ("Cows", string.ascii_letters, "Cows"),
        ("Cows are Fun", string.whitespace + string.ascii_letters, "Cows are Fun"),
        ("\t\t", string.printable, "\t\t"),
        ("\t\t", string.ascii_letters, ""),
        ("\a123", string.printable, "123"),
        (None, string.printable, ""),
    ],
)
def test_safe_to_text(inText: str, valid: str, expected: str):
    actual = ConvertHelpers.safe_to_text(inText, valid)
    # assert actual == expected
