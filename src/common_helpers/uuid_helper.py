import uuid


class UuidHelper:
    """
    UUID helpers
    """

    @staticmethod
    def is_valid_uuid(input_text: str) -> bool:
        """
        checks to see if a string is a valid UUID

        Args:
            val (str): (sic)

        Returns:
            bool: True if so
        """
        try:
            uuid_obj = uuid.UUID(str(input_text))
        except ValueError:
            return False

        return str(uuid_obj) == input_text

    @staticmethod
    def to_uuid(input_text) -> uuid.UUID:
        """
        Returns UUID or nil (all zeros)

        Args:
            input_text: (sic)

        Returns:
            uuid.UUID: converted or nil
        """
        try:
            return uuid.UUID(str(input_text))
        except ValueError:
            return uuid.NIL

    @staticmethod
    def from_uuid(u: uuid.UUID) -> str:
        """
        returns standardized uuid string

        Args:
            u (uuid.UUID): (sic)

        Returns:
            str: (sic)
        """
        return str(u)
