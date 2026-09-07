import bcrypt


class AuthLibrary:
    """Manages secure database operations and password hashing."""

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
