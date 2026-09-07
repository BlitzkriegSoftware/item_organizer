import pytest

from security_lib.fermet_helper import FermetHelper


def fermet_test_round_trip():
    expected = "the quick brown fox jumped over the lazy dog."
    key = FermetHelper.generate_key()

    cyphered = FermetHelper.encrypt_message(expected, key)
    actual = FermetHelper.decrypt_message(cyphered, key)

    assert expected == actual
