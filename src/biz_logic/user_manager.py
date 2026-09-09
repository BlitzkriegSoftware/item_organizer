from datetime import timezone, datetime
import os


from app_exceptions.configuration_exception import ConfigurationException
from app_exceptions.db_exception import DatabaseException
from app_exceptions.security_exception import SecurityException
from app_exceptions.validation_exception import ValidationException
from biz_logic.user_status import UserStatus
from common_helpers.convert_helpers import ConvertHelpers
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
    VALID_USER_ORG_ROLE_IDS = [0, 1, 2, 4, 8, 16]

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
        if not IOR_SALT:  # pragma: no cover
            raise ConfigurationException("Salt Required", "IOR_SALT", "env")

        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("Schema Required", "IOR_SCHEMA", "env")

        query = f"select password_hash from {IOR_SCHEMA}.user where email='{email}';"

        hashed = DataLib.query_return_single_value_in_one(query)
        if not hashed:
            raise SecurityException("User not found", email)  # pragma: no cover

        result = AuthLibrary.Verify_Password(password, hashed)
        if not result:
            raise SecurityException("Invalid Login", email)  # pragma: no cover

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
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("Schema Required", "IOR_SCHEMA", "env")

        if not email:  # pragma: no cover
            raise ValidationException("must not be empty", "email")

        if not TypeValidators.is_email(email):  # pragma: no cover
            raise ValidationException("malformed", f"email: {email}")

        if not fullname:  # pragma: no cover
            raise ValidationException("must not be empty", "email")

        if icon_url:  # pragma: no cover
            if not TypeValidators.is_url(icon_url):
                raise ValidationException("malformed", f"icon_url: {icon_url}")

        query = (
            f"select user_display_name from {IOR_SCHEMA}.user where email='{email}';"
        )
        result = DataLib.query_return_dict_in_one(query)
        if DataLib.has_rows(result):  # pragma: no cover
            raise SecurityException("User exists already", email)

        query = f"insert into {IOR_SCHEMA}.user (email, user_display_name, user_icon_uri, password_hash) values ('{email}','{fullname}','{icon_url}','{UserStatus.CONFIRM}');"
        print("query: ", query)
        result = DataLib.query_execute_in_one(query)
        if not result:  # pragma: no cover
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
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("Schema Required", "IOR_SCHEMA", "env")

        if not email:  # pragma: no cover
            raise ValidationException("must not be empty", "email")

        if not TypeValidators.is_email(email):  # pragma: no cover
            raise ValidationException("malformed", f"email: {email}")

        query = f"update {IOR_SCHEMA}.user set password_hash ='{UserStatus.DISABLED}' where email = '{email}';"
        result = DataLib.query_execute_in_one(query)
        if not result:  # pragma: no cover
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
        if not IOR_FERMAT:  # pragma: no cover
            raise ConfigurationException("CryptoKey Required", "IOR_FERMAT", "env")

        if not email:  # pragma: no cover
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
        """validate hash

        Args:
            email (str): (sic)
            hashed (str): previously generated hash
            limit (int, optional): In minutes. Defaults to RESET_STAMP_TOLERANCE_MINUTES.

        Raises:
            ConfigurationException: IOR_FERMAT
            ValidationException: email missing
            ValidationException: hash missing
            ValidationException: hash not base64
            ValidationException: hash corrupt (0)
            ValidationException: hash corrupt (1)
            ValidationException: hash corrupt (2)
            ValidationException: hash expired (3)
        """
        IOR_FERMAT = os.getenv("IOR_FERMAT", "")
        if not IOR_FERMAT:  # pragma: no cover
            raise ConfigurationException("CryptoKey Required", "IOR_FERMAT", "env")

        if not email:  # pragma: no cover
            raise ValidationException("Empty", "email")

        if not hashed:  # pragma: no cover
            raise ValidationException("Empty", "hashed")

        if not Base64Helper.is_base64(hashed):  # pragma: no cover
            raise ValidationException("Provided hash corrupt (0)", "hashed")

        plain_text = FermetHelper.decrypt_message(hashed)

        fields = plain_text.split("/")
        if not fields or len(fields) < 2:  # pragma: no cover
            raise ValidationException("Provided hash corrupt (1)", "hashed")

        if fields[0].casefold() != email.casefold():  # pragma: no cover
            raise ValidationException("Provided hash corrupt (2)", "hashed")

        dtnow = datetime.now(timezone.utc)
        dtstamp = DateTimeHelpers.from_iso8601(fields[1])
        diff = dtnow - dtstamp
        whole_minutes = int(diff.total_seconds() // 60)
        if whole_minutes > limit:  # pragma: no cover
            raise ValidationException("Provided hash expired (3)", "hashed")

    @staticmethod
    def user_status(email: str) -> UserStatus:
        """
        Gets user status

        Args:
            email (str): (sic)

        Returns:
            UserStatus: Enum
        """
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("Schema Required", "IOR_SCHEMA", "env")

        query = f"select password_hash from {IOR_SCHEMA}.user where email = '{email}';"
        result = DataLib.query_return_single_value_in_one(query)

        if not result:
            return UserStatus.NOTUSER

        result = str(result)

        if UserStatus.CONFIRM.casefold() in result.casefold():
            return UserStatus.CONFIRM

        if UserStatus.DISABLED.casefold() in result.casefold():
            return UserStatus.DISABLED

        return UserStatus.ACTIVE

    @staticmethod
    def user_remove_last_resort(email: str):
        """yank user forceable, reassign all items to admin

        Args:
            email (str): (sic)

        Raises:
            ConfigurationException: IOR_SCHEMA
            ValidationException: email missing
            DatabaseException: execution failure
        """
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("Schema Required", "IOR_SCHEMA", "env")

        if not email:  # pragma: no cover
            raise ValidationException("Empty", "email")

        procedure_name = "user_force_remove"
        args = (email,)
        isOk = DataLib.stored_procedure_execute_all_in_one(
            procedure_name, args, IOR_SCHEMA
        )
        if not isOk:  # pragma: no cover
            raise DatabaseException("Execution Failure", procedure_name)

    @staticmethod
    def user_org_add_by_email(
        email: str,
        org_id: int,
        org_role_id: int,
    ):
        """add user to org

        Args:
            email (str): (sic)
            org_id (int): _(sic)
            org_role_id (int): must be valid in UserManager.VALID_USER_ORG_ROLE_IDS

        Raises:
            ConfigurationException: IOR_SCHEMA
            ValueError: email missing
            SecurityException: user not found
            SecurityException: invalid org role id
        """
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("Schema Required", "IOR_SCHEMA", "env")

        if not email:  # pragma: no cover
            raise ValueError("email required")

        query = f"select user_id from {IOR_SCHEMA}.user where email ='{email}';"
        user_id = DataLib.query_return_single_value_in_one(query)
        if not user_id:  # pragma: no cover
            raise SecurityException("user not found (0)", email)

        user_id = ConvertHelpers.safe_to_int(user_id, -1)
        if user_id < 0:  # pragma: no cover
            raise SecurityException("user not found (1)", email)

        UserManager.user_org_add_by_id(user_id, org_id, org_role_id)

    @staticmethod
    def user_org_add_by_id(
        user_id: int,
        org_id: int,
        org_role_id: int,
    ):
        """add to org by id

        Args:
            user_id (int): (sic)
            org_id (int): _(sic)
            org_role_id (int): must be valid in UserManager.VALID_USER_ORG_ROLE_IDS

        Raises:
            ConfigurationException: IOR_SCHEMA 
            ValueError: invalid org role id
            SecurityException:  unable(0)
            SecurityException:  unable(1)
        """
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("Schema Required", "IOR_SCHEMA", "env")

        if org_role_id not in UserManager.VALID_USER_ORG_ROLE_IDS:
            raise ValueError(
                f"org role id must be in {UserManager.VALID_USER_ORG_ROLE_IDS} (1)"
            )

        query = f"delete from {IOR_SCHEMA}.user_org where user_id = {user_id} and org_id = {org_id};"
        result = DataLib.query_execute_in_one(query)
        if not result:  # pragma: no cover
            raise SecurityException("Unable (0)", query)

        query = f"insert into {IOR_SCHEMA}.user_org (user_id, org_id, org_role_id) values ({user_id},{org_id},{org_role_id})"
        result = DataLib.query_execute_in_one(query)
        if not result:  # pragma: no cover
            raise SecurityException("Unable (1)", query)

    @staticmethod
    def user_org_remove_by_email(
        email: str,
        org_id: int,
    ):
        """
        remove roles for user in org

        Args:
            email (str): (sic)
            org_id (int): (sic)

        Raises:
            ConfigurationException: IOR_SCHEMA
            ValueError: bad email
            SecurityException: (unable)
        """
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("Schema Required", "IOR_SCHEMA", "env")

        if not email:  # pragma: no cover
            raise ValueError("email required")

        query = f"select user_id from {IOR_SCHEMA}.user where email='{email}';"
        user_id = DataLib.query_return_single_value_in_one(query)
        if not user_id:  # pragma: no cover
            raise SecurityException("user not found", email)

        UserManager.user_org_remove_by_id(user_id, org_id)

    @staticmethod
    def user_org_remove_by_id(
        user_id: int,
        org_id: int,
    ):
        """
        Removes a users org roles

        Args:
            user_id (int): (sic)
            org_id (int): (sic)

        Raises:
            ConfigurationException: IOR_SCHEMA
            SecurityException: (unable)
        """
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("Schema Required", "IOR_SCHEMA", "env")

        query = f"delete from {IOR_SCHEMA}.user_org where user_id = {user_id} and org_id = {org_id};"
        result = DataLib.query_execute_in_one(query)
        if not result:  # pragma: no cover
            raise SecurityException("Unable", query)

    @staticmethod
    def user_org_role_get_by_email(
        email: str,
        org_id: int,
    ):
        """
        Look up Org_Role_Id by email

        Args:
            email (str): (sic)
            org_id (int): (sic)

        Raises:
            ConfigurationException: IOR_SCHEMA
            SecurityException: Bad Role Assignment

        Returns:
            int: Org_Role_Id
        """
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("Schema Required", "IOR_SCHEMA", "env")

        query = f"select user_id from {IOR_SCHEMA}.user where email='{email}';"
        user_id = DataLib.query_return_single_value_in_one(query)
        if not user_id:  # pragma: no cover
            raise SecurityException("user not found", email)

        return UserManager.user_org_role_get_by_id(user_id, org_id)

    @staticmethod
    def user_org_role_get_by_id(
        user_id: int,
        org_id: int,
    ) -> int:
        """
        get user's role in org
        recursive upwards

        Args:
            user_id (int): (sic)
            org_id (int): (sic)

        Raises:
            ConfigurationException: IOR_SCHEMA
            SecurityException: Bad Role Assignment

        Returns:
            int: Org_Role_Id
        """
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("Schema Required", "IOR_SCHEMA", "env")

        query = f"select {IOR_SCHEMA}.user_org_role_get({user_id}, {org_id});"
        result = DataLib.query_return_single_value_in_one(query)
        if not result:  # pragma: no cover
            return 0  # no role

        user_role_id = ConvertHelpers.safe_to_int(result, 0)

        if user_role_id not in UserManager.VALID_USER_ORG_ROLE_IDS:  # pragma: no cover
            raise SecurityException("Bad Role Id", str(user_role_id))

        return user_role_id
