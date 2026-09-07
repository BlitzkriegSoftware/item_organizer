from cryptography.fernet import Fernet


class FermetHelper:
    @staticmethod
    def generate_key() -> bytes:
        """Generates a secure key for encryption and decryption."""
        return Fernet.generate_key()

    @staticmethod
    def encrypt_message(message: str, key: bytes) -> bytes:
        """Encrypts a string message using the provided key."""
        # Convert the string to bytes
        encoded_message = message.encode("utf-8")

        # Initialize Fernet with the key
        f = Fernet(key)

        # Encrypt the token
        encrypted_message = f.encrypt(encoded_message)
        return encrypted_message

    @staticmethod
    def decrypt_message(encrypted_message: bytes, key: bytes) -> str:
        """Decrypts an encrypted byte token back into a string message."""
        # Initialize Fernet with the key
        f = Fernet(key)

        # Decrypt the token
        decrypted_bytes = f.decrypt(encrypted_message)

        # Decode the bytes back to a readable string
        return decrypted_bytes.decode("utf-8")
