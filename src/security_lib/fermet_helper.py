import os

from cryptography.fernet import Fernet

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
        key = FermetHelper.generate_key()
        return Base64Helper.to_base64(key)

    @staticmethod
    def encrypt_message(message: str) -> str:
        if not message:
            raise ValueError("message required")

        IOR_FERMAT = os.getenv("IOR_FERMAT", "")
        if not IOR_FERMAT:
            raise ConfigurationException("Cypther key must be set", "IOR_FERMET")

        if Base64Helper.is_base64(IOR_FERMAT):
            key = Base64Helper.from_base64(IOR_FERMAT)
        else:
            raise ValidationException("Expected b64", "IOR_FERMAT")

        cyphered = FermetHelper.encrypt_message_bytes(message, key)

        return Base64Helper.to_base64(cyphered)

    @staticmethod
    def encrypt_message_bytes(message: str, key: bytes) -> bytes:
        """Encrypts a string message using the provided key."""
        # Convert the string to bytes
        encoded_message = message.encode("utf-8")

        # Initialize Fernet with the key
        f = Fernet(key)

        # Encrypt the token
        encrypted_message = f.encrypt(encoded_message)
        return encrypted_message

    @staticmethod
    def decrypt_message(cypher_b64: str) -> str:
        if not cypher_b64:
            raise ValueError("cypher text required")

        IOR_FERMAT = os.getenv("IOR_FERMAT", "")
        if not IOR_FERMAT:
            raise ConfigurationException("Cypther key must be set", "IOR_FERMET")

        if Base64Helper.is_base64(IOR_FERMAT):
            key = Base64Helper.from_base64(IOR_FERMAT)
        else:
            raise ValidationException("Expected b64", "IOR_FERMAT")

        cyther_bytes = Base64Helper.from_base64(cypher_b64)

        plain_text = FermetHelper.decrypt_message_bytes(cyther_bytes, key)

        return plain_text

    @staticmethod
    def decrypt_message_bytes(encrypted_message: bytes, key: bytes) -> str:
        """Decrypts an encrypted byte token back into a string message."""
        # Initialize Fernet with the key
        f = Fernet(key)

        # Decrypt the token
        decrypted_bytes = f.decrypt(encrypted_message)

        # Decode the bytes back to a readable string
        return decrypted_bytes.decode("utf-8")
