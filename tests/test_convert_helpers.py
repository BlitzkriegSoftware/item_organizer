from common_helpers.convert_helpers import ConvertHelpers


def test_safe_to_int_1():
    v = ConvertHelpers.safe_to_int(1, 0)
    assert v == 1


def test_safe_to_int_bad():
    v = ConvertHelpers.safe_to_int("cows", 0)
    assert v == 0
