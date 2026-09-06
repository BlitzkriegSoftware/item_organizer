import os

from app_exceptions import ConfigurationException
from security import AuthManager


class UserManager:
    """
    Manager Users
    """

    @staticmethod
    def Login(email: str, password: str):
        IOR_SALT = os.getenv("IOR_SALT", "")
        if not IOR_SALT:
            raise ConfigurationException("Salt Required", "IOR_SALT", "env")

        result = AuthManager.Verify_Password(password)
