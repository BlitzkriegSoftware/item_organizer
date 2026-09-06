import base64
import binascii


class Base64Helper:
    """
    Handy base64 utilities

    """

    @staticmethod
    def to_base64(raw_bytes: bytes) -> str:
        """
        bytes => base64 string

        Args:
            raw_bytes (bytes): IN

        Returns:
            str: OUT
        """
        b64_bytes = base64.b64encode(raw_bytes)
        b64_string = b64_bytes.decode("utf-8")
        return b64_string

    @staticmethod
    def to_base64_s(text: str) -> str:
        """
        text => base65

        Args:
            text (str): IN

        Returns:
            str: OUT
        """
        raw_bytes = text.encode("utf-8")
        return Base64Helper.to_base64(raw_bytes)

    @staticmethod
    def from_base64(b64_string: str) -> bytes:
        """
        base64 => bytes

        Args:
            b64_string (str): IN

        Returns:
            bytes: OUT
        """
        original_bytes = base64.b64decode(b64_string)
        return original_bytes

    @staticmethod
    def from_base64_s(b64_string: str) -> str:
        """
        base64 => plain text

        Args:
            b64_string (str): IN

        Returns:
            bytes: OUT
        """
        original_bytes = Base64Helper.from_base64(b64_string)
        return original_bytes.decode("utf-8")

    @staticmethod
    def is_base64(s: str) -> bool:
        """
        Is this string base64 encoded?

        Args:
            s (str): text to test

        Returns:
            bool: true if so
        """
        try:
            # Convert the string to bytes and decode with strict validation
            base64.b64decode(s, validate=True)
            return True
        except (binascii.Error, ValueError):
            # A binascii.Error is raised if padding or characters are invalid
            return False
