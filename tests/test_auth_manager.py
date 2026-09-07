import pytest
import os
from security_lib.auth_library import AuthLibrary
from common_helpers.base64_helpers import Base64Helper


def test_salt_round_trip():
    salt1 = AuthLibrary.Make_Salt()
    salthash = Base64Helper.to_base64(salt1)
    salt2 = Base64Helper.from_base64(salthash)
    assert salt1 == salt2


def test_hash_password():
    fromenv: bool = False
    salthash = os.getenv("IOR_SALT")
    if salthash:
        salt1 = Base64Helper.from_base64(salthash)
        fromenv = True
    else:
        salt1 = AuthLibrary.Make_Salt()

    salthash = Base64Helper.to_base64(salt1)
    print("Salt ->", salthash, "<-, from ENV: ", fromenv)

    password = "password123-"
    hashed = AuthLibrary.Hash_Password(salt1, password)
    print("Password: ", password, "=>", hashed, "<=")
    assert len(hashed) > 0


def test_verify_password():
    salt = AuthLibrary.Make_Salt()
    password = "password123-"
    hashed = AuthLibrary.Hash_Password(salt, password)
    result = AuthLibrary.Verify_Password(password, hashed)
    assert result
