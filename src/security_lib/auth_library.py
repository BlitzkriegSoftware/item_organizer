from functools import cache
import os

import bcrypt

from app_exceptions.configuration_exception import ConfigurationException
from common_helpers.base64_helpers import Base64Helper


class AuthLibrary:
    """Manages secure database operations and password hashing."""

    @cache
    @staticmethod
    def ior_salt_get() -> str:
        """
        Gets Authentication SALT

        Raises:
            ConfigurationException: if not found

        Returns:
            str: encoded salt
        """
        IOR_SALT = os.getenv("IOR_SALT")
        if not IOR_SALT:
            raise ConfigurationException("Authentication SALT must be set", "IOR_SALT")

        return IOR_SALT

    @cache
    @staticmethod
    def salt_str_to_bytes(salthash: str) -> bytes:
        if salthash:
            salt1 = Base64Helper.from_base64(salthash)
        else:
            salt1 = b""

        return salt1

    @staticmethod
    def Make_Salt() -> bytes:
        hash_rounds: int = 12
        salt = bcrypt.gensalt(rounds=hash_rounds)
        return salt

    @staticmethod
    def Hash_Password(salt: bytes, password: str) -> str:
        """Hashes a plain-text password using bcrypt with a salt."""
        # Convert string to bytes
        password_bytes = password.encode("utf-8")
        hashed_bytes = bcrypt.hashpw(password_bytes, salt)
        # Store as string in the database
        return hashed_bytes.decode("utf-8")

    @staticmethod
    def Verify_Password(plain_password: str, hashed_password: str) -> bool:
        """Verifies a plain-text password against the stored bcrypt hash."""
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
