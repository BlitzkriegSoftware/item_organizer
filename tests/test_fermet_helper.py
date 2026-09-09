import os

import pytest

from common_helpers.base64_helpers import Base64Helper
from security_lib.fermet_helper import FermetHelper


def test_fermet_round_trip():
    expected = "the quick brown fox jumped over the lazy dog."

    from_env: bool = False
    IOR_FERMAT = os.getenv("IOR_FERMAT", "")
    key: bytes = b""
    if IOR_FERMAT:
        from_env = True
        if Base64Helper.is_base64(IOR_FERMAT):
            key = Base64Helper.from_base64(IOR_FERMAT)
        else:
            key = IOR_FERMAT.encode("utf8")
    else:
        key = FermetHelper.generate_key()
        IOR_FERMAT = Base64Helper.to_base64(key)

    print(f"setx IOR_FERMAT '{IOR_FERMAT}' # From Env {from_env}")

    expected_bytes = expected.encode("utf-8")

    cyphered = FermetHelper.encrypt_bytes(expected_bytes, key)
    
    actual_bytes = FermetHelper.decrypt_bytes(cyphered, key)
    actual = actual_bytes.decode("utf-8")
    assert expected == actual


def test_round_trip_env_key():
    expected = "the quick brown fox jumped over the lazy dog."
    cyphered = FermetHelper.encrypt_message(expected)
    actual = FermetHelper.decrypt_message(cyphered)
    assert expected == actual
