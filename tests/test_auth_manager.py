import pytest
from Security.AuthManager import AuthManager


def test_hash_password():
    password = "password123-"
    hashed = AuthManager.Hash_Password(password)
    assert len(hashed) > 0


def test_verify_password():
    password = "password123-"
    hashed = AuthManager.Hash_Password(password)
    result = AuthManager.Verify_Password(password, hashed)
    assert result
