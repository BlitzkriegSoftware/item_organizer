import re
import string


class TypeValidators:
    """
    Type Validators
    """

    @staticmethod
    def is_email(email: str) -> bool:
        """
        Checks for well formed e-mail

        Args:
            email (str): (sic)

        Returns:
            bool: True if so
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        result = re.fullmatch(pattern, email)
        return result is not None

    @staticmethod
    def is_url(url: str) -> bool:
        """
        Check to see if valid url

        Args:
            url (str): (sic)

        Returns:
            bool: True if so
        """
        pattern = r"^(https?):\/\/([a-zA-Z0-9.-]+)(:[0-9]+)?(\/[a-zA-Z0-9._~:/?#\[\]@!$&'()*+,;=-]*)?$"
        result = re.fullmatch(pattern, url)
        return result is not None

    @staticmethod
    def has_only(text: str, validChars: str = string.printable) -> bool:
        """
        Has Only Valid Characters

        See: https://docs.python.org/3/library/string.html

        Args:
            text (str): text to check
            validChars (str, optional): (sic) Defaults to string.printable.

        Returns:
            bool: True if so
        """
        if not text:  # pragma: no cover
            return False
        for letter in text:
            if letter not in validChars:
                return False

        return True
