import bcrypt


class AuthManager:
    """Manages secure database operations and password hashing."""

    @staticmethod
    def Hash_Password(password: str) -> str:
        """Hashes a plain-text password using bcrypt with a random salt."""
        hash_rounds: int = 12
        # Convert string to bytes
        password_bytes = password.encode("utf-8")
        # Generate salt and hash (bcrypt handles salt generation internally here)
        hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=hash_rounds))
        # Store as string in the database
        return hashed_bytes.decode("utf-8")

    @staticmethod
    def Verify_Password(plain_password: str, hashed_password: str) -> bool:
        """Verifies a plain-text password against the stored bcrypt hash."""
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
