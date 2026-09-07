import datetime
import os

from app_exceptions.configuration_exception import ConfigurationException
from app_exceptions.security_exception import SecurityException
from app_exceptions.validation_exception import ValidationException
from common_helpers.type_validators import TypeValidators
from data_lib.datalib import DataLib
from security_lib.auth_manager import AuthManager
from common_helpers.base64_helpers import Base64Helper


class UserManager:
    """
    Manager Users
    """

    PASSWORD_HASH_NEEDS_CONFIRM = "CONFIRM"
    PASSWORD_HASH_DISABLED = "DISABLED"

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

    @staticmethod
    def add_user(
        email: str,
        fullname: str,
        icon_url: str,
    ):
        """
        add_user but can not login

        Args:
            email (str): (sic)
            fullname (str): (sic)
            icon_url (str): (optional)

        Raises:
            ConfigurationException: IOR_SCHEMA
            ValidationException: email missing
            ValidationException: email malformed
            ValidationException: fullname missing
            ValidationException: icon_url malformed
            SecurityException: unable to add user
        """
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")
        if not IOR_SCHEMA:
            raise ConfigurationException("Schema Required", "IOR_SCHEMA", "env")

        if not email:
            raise ValidationException("must not be empty", "email")

        if not TypeValidators.is_email(email):
            raise ValidationException("malformed", f"email: {email}")

        if not fullname:
            raise ValidationException("must not be empty", "email")

        if icon_url:
            if not TypeValidators.is_url(icon_url):
                raise ValidationException("malformed", f"icon_url: {icon_url}")

        query = f"insert into {IOR_SCHEMA}.user (email, user_display_name, user_icon_uri, password_hash) values ('{email}','{fullname}','{icon_url}','{UserManager.PASSWORD_HASH_NEEDS_CONFIRM}');"
        result = DataLib.query_execute_in_one(query)
        if not result:
            raise SecurityException("Unable to add user", email)

    @staticmethod
    def disable_user(
        email: str,
    ):
        """
        Disables user by zozting password hash

        Args:
            email (str): (sic)

        Raises:
            ConfigurationException: IOR_SCHEMA
            ValidationException: email missing
            ValidationException: email malformed
            SecurityException: unable to disable
        """
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")
        if not IOR_SCHEMA:
            raise ConfigurationException("Schema Required", "IOR_SCHEMA", "env")

        if not email:
            raise ValidationException("must not be empty", "email")

        if not TypeValidators.is_email(email):
            raise ValidationException("malformed", f"email: {email}")

        query = f"update {IOR_SCHEMA}.user set password_hash ='{UserManager.PASSWORD_HASH_DISABLED}' where email = '{email}';"
        result = DataLib.query_execute_in_one(query)
        if not result:
            raise SecurityException("Unable to disable user", email)

    @staticmethod
    def generate_reset_hash(email):
        stamp = datetime.
