import os

from app_exceptions.configuration_exception import ConfigurationException
from app_exceptions.security_exception import SecurityException
from data_lib.datalib import DataLib
from security_lib.auth_manager import AuthManager
from common_helpers.base64_helpers import Base64Helper


class UserManager:
    """
    Manager Users
    """

    @staticmethod
    def login(email: str, password: str):
        """
        Does login

        Args:
            email (str): (sic)
            password (str): plain text password

        Raises:
            ConfigurationException: missing salt
            ConfigurationException: missing schema
            SecurityException: user not found
            SecurityException: bad login
        """
        IOR_SALT = os.getenv("IOR_SALT", "")
        if not IOR_SALT:
            raise ConfigurationException("Salt Required", "IOR_SALT", "env")

        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")
        if not IOR_SCHEMA:
            raise ConfigurationException("Schema Required", "IOR_SCHEMA", "env")

        query = f"select password_hash from {IOR_SCHEMA}.user where email='{email}';"

        hashed = DataLib.query_return_single_value_in_one(query)
        if not hashed:
            raise SecurityException("User not found", email)

        result = AuthManager.Verify_Password(password, hashed)
        if not result:
            raise SecurityException("Invalid Login", email)
