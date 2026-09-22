import pytest

from app_exceptions.configuration_exception import ConfigurationException
from app_exceptions.db_exception import DatabaseException
from app_exceptions.policy_exception import PolicyException
from app_exceptions.security_exception import SecurityException
from app_exceptions.validation_exception import ValidationException


def test_configuration_exception():
    ex = ConfigurationException("message", "xre", "cmd")
    print(ex)


def test_db_exception():
    ex = DatabaseException("message", "select from...")
    print(ex)


def test_security_exception():
    ex = SecurityException("message", "bad developer")
    print(ex)


def test_validation_exception():
    ex = ValidationException("message", "field1", "value")
    print(ex)


def test_policy_exception():
    ex = PolicyException("message", "policy")
    print(ex)
