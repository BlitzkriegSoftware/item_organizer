import pytest
import os
from Security.AuthManager import AuthManager


def test_salt_round_trip():
    salt1 = AuthManager.Make_Salt()
    salthash = AuthManager.To_Base64(salt1)
    salt2 = AuthManager.From_Base64(salthash)
    assert salt1 == salt2


def test_hash_password():
    fromenv: bool = False
    salthash = os.getenv("IOR_SALT")
    if salthash:
        salt1 = AuthManager.From_Base64(salthash)
        fromenv = True
    else:
        salt1 = AuthManager.Make_Salt()

    salthash = AuthManager.To_Base64(salt1)
    print("Salt ->", salthash, "<-, from ENV: ", fromenv)

    password = "password123-"
    hashed = AuthManager.Hash_Password(salt1, password)
    print("Password: ", password, "=>", hashed, "<=")
    assert len(hashed) > 0


def test_verify_password():
    salt = AuthManager.Make_Salt()
    password = "password123-"
    hashed = AuthManager.Hash_Password(salt, password)
    result = AuthManager.Verify_Password(password, hashed)
    assert result
