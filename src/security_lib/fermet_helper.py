import os

from cryptography.fernet import Fernet
from varname import nameof

from app_exceptions.configuration_exception import ConfigurationException
from app_exceptions.validation_exception import ValidationException
from common_helpers.base64_helpers import Base64Helper


class FermetHelper:
    @staticmethod
    def generate_key() -> bytes:
        """Generates a secure key for encryption and decryption."""
        return Fernet.generate_key()

    @staticmethod
    def generate_key_b64() -> str:
        """Generates key as Base64
        Returns:
            str: base64 encoded key
        """
        key = FermetHelper.generate_key()
        return Base64Helper.to_base64(key)

    @staticmethod
    def encrypt_message(message: str) -> str:
        """Encrypt text

        Args:
            message (str): plain text to encrypt

        Raises:
            ValueError: missing message
            ConfigurationException: IOR_FERMAT
            ValidationException: not base64

        Returns:
            str: base64 encoded encrypted text
        """
        if not message: # pragma: no cover
            raise ValueError("message required")

        IOR_FERMAT = os.getenv("IOR_FERMAT", "")
        if not IOR_FERMAT:  # pragma: no cover
            raise ConfigurationException("Cypther key must be set", "IOR_FERMET")

        if Base64Helper.is_base64(IOR_FERMAT):
            key = Base64Helper.from_base64(IOR_FERMAT)
        else:  # pragma: no cover
            raise ValidationException("Expected b64", nameof(IOR_FERMAT), IOR_FERMAT)

        message_bytes = message.encode("utf-8")

        cyphered = FermetHelper.encrypt_bytes(message_bytes, key)

        return Base64Helper.to_base64(cyphered)

    @staticmethod
    def decrypt_message(cypher_b64: str) -> str:
        """decrypt

        Args:
            cypher_b64 (str): base64 encoded cypher text

        Raises:
            ValueError: missing cypher text
            ConfigurationException: IOR_FERMAT
            ValidationException: not base64

        Returns:
            str: _description_
        """
        if not cypher_b64:  # pragma: no cover
            raise ValueError("cypher text required")

        IOR_FERMAT = os.getenv("IOR_FERMAT", "")
        if not IOR_FERMAT:  # pragma: no cover
            raise ConfigurationException("Cypther key must be set", "IOR_FERMET")

        if Base64Helper.is_base64(IOR_FERMAT):
            key = Base64Helper.from_base64(IOR_FERMAT)
        else: # pragma: no cover
            raise ValidationException("Expected b64", nameof(IOR_FERMAT), IOR_FERMAT)

        if Base64Helper.is_base64(cypher_b64):
            cypher_bytes = Base64Helper.from_base64(cypher_b64)
        else: # pragma: no cover
            cypher_bytes = cypher_b64.encode("utf-8")

        decrypted_bytes = FermetHelper.decrypt_bytes(cypher_bytes, key)

        plain_text = decrypted_bytes.decode("utf-8")

        return plain_text

    @staticmethod
    def encrypt_bytes(message_bytes: bytes, key: bytes) -> bytes:
        """encrypt bytes

        Args:
            message (bytes): bytes to encrypt
            key (bytes): key to use for encryption

        Returns:
            bytes: encrypted bytes
        """

        # Initialize Fernet with the key
        f = Fernet(key)

        # Encrypt the token
        encrypted_message = f.encrypt(message_bytes)
        return encrypted_message

    @staticmethod
    def decrypt_bytes(encrypted_message: bytes, key: bytes) -> bytes:
        """Decrypts an encrypted byte token back into a string message."""
        # Initialize Fernet with the key
        f = Fernet(key)

        # Decrypt the token
        decrypted_bytes = f.decrypt(encrypted_message)

        # Return the decrypted bytes
        return decrypted_bytes
