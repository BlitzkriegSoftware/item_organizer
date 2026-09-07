from datetime import timezone, datetime
import os

import pytest

from app_exceptions.configuration_exception import ConfigurationException
from app_exceptions.security_exception import SecurityException
from app_exceptions.validation_exception import ValidationException
from biz_logic.user_status import UserStatus
from common_helpers.datetime_helpers import DateTimeHelpers
from common_helpers.type_validators import TypeValidators
from data_lib.datalib import DataLib
from security_lib.auth_library import AuthLibrary
from common_helpers.base64_helpers import Base64Helper
from security_lib.fermet_helper import FermetHelper


class UserManager:
    """
    Manager Users
    """

    RESET_STAMP_TOLERANCE_MINUTES = 30

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

        result = AuthLibrary.Verify_Password(password, hashed)
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

        query = (
            f"select user_display_name from {IOR_SCHEMA}.user where email='{email}';"
        )
        result = DataLib.query_return_dict_in_one(query)
        if DataLib.has_rows(result):
            raise SecurityException("User exists already", email)

        query = f"insert into {IOR_SCHEMA}.user (email, user_display_name, user_icon_uri, password_hash) values ('{email}','{fullname}','{icon_url}','{UserStatus.CONFIRM}');"
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

        query = f"update {IOR_SCHEMA}.user set password_hash ='{UserStatus.DISABLED}' where email = '{email}';"
        result = DataLib.query_execute_in_one(query)
        if not result:
            raise SecurityException("Unable to disable user", email)

    @staticmethod
    def generate_reset_hash(
        email: str,
        hash_at: datetime = datetime.now(timezone.utc),
    ):
        """
        generates a reset hash that can be used in an e-mail

        Args:
            email (str): (sic)
            hash_at (datetime, optional): Expiration. Defaults to datetime.now(timezone.utc).

        Raises:
            ConfigurationException: if IOR_FERMAT is missing
            ValidationException: if email is missing

        Returns:
            _type_: b64 embeddable secret
        """
        IOR_FERMAT = os.getenv("IOR_FERMAT", "")
        if not IOR_FERMAT:
            raise ConfigurationException("CryptoKey Required", "IOR_FERMAT", "env")

        if not email:
            raise ValidationException("Empty", "email")

        stamp = DateTimeHelpers.to_iso8601_with_z(hash_at)
        mash = f"{email}/{stamp}"
        hashed = FermetHelper.encrypt_message(mash)
        return hashed

    @staticmethod
    def validate_reset_hash(
        email: str,
        hashed: str,
        limit: int = RESET_STAMP_TOLERANCE_MINUTES,
    ):
        IOR_FERMAT = os.getenv("IOR_FERMAT", "")
        if not IOR_FERMAT:
            raise ConfigurationException("CryptoKey Required", "IOR_FERMAT", "env")

        if not email:
            raise ValidationException("Empty", "email")

        if not hashed:
            raise ValidationException("Empty", "hashed")

        if not Base64Helper.is_base64(hashed):
            raise ValidationException("Not base64", "hashed")

        plain_text = FermetHelper.decrypt_message(hashed)

        fields = plain_text.split("/")
        if not fields or len(fields) < 2:
            raise ValidationException("Provided hash corrupt", "hashed")

        if fields[0].casefold() != email.casefold():
            raise ValidationException("Provided hash corrupt[0]", "hashed")

        dtnow = datetime.now(timezone.utc)
        dtstamp = DateTimeHelpers.from_iso8601(fields[1])
        diff = dtnow - dtstamp
        whole_minutes = int(diff.total_seconds() // 60)
        if whole_minutes > limit:
            raise ValidationException("Provided hash expired", "hashed")

    @staticmethod
    def user_status(email: str) -> UserStatus:
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")
        if not IOR_SCHEMA:
            pytest.fail("IOR_SCHEMA missing")

        query = f"select password_hash from {IOR_SCHEMA}.user where email = '{email}';"
        result = DataLib.query_return_single_value_in_one(query)
        result = str(result)

        if not result:
            return UserStatus.NOTUSER

        if UserStatus.CONFIRM.casefold() in result.casefold():
            return UserStatus.CONFIRM

        if UserStatus.DISABLED.casefold() in result.casefold():
            return UserStatus.DISABLED

        return UserStatus.ACTIVE
