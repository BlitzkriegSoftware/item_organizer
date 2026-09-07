import os

import pytest

from common_helpers.base64_helpers import Base64Helper
from security_lib.fermet_helper import FermetHelper


def test_fermet_round_trip():
    expected = "the quick brown fox jumped over the lazy dog."

    from_env: bool = False
    IOR_FERMAT = os.getenv("IOR_FERMAT", "")
    if IOR_FERMAT:
        from_env = True
        if Base64Helper.is_base64(IOR_FERMAT):
            key = Base64Helper.from_base64(IOR_FERMAT)
        else:
            key = IOR_FERMAT
    else:
        key = FermetHelper.generate_key()
        IOR_FERMAT = Base64Helper.to_base64(key)

    print(f"setx IOR_FERMAT '{IOR_FERMAT}' # From Env {from_env}")

    cyphered = FermetHelper.encrypt_message(expected, key)
    actual = FermetHelper.decrypt_message(cyphered, key)
    assert expected == actual
