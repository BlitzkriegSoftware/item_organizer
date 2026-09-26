from typing import Any
import string


class ConvertHelpers:
    @staticmethod
    def safe_to_int(the_value: Any, the_default: int) -> int:
        """
        Safely convert to int

        Args:
            the_value (Any): IN
            the_default (int): DEFAULT

        Returns:
            int: Converted
        """
        return_value = the_default
        try:
            return_value = int(the_value)
        except:  # noqa: E722 # pragma: no cover
            return_value = the_default
        return return_value

    @staticmethod
    def clean_text(text: str, valid: str = string.printable) -> str:
        """
        clean text of unwanted characters

        Args:
            text (str): (sic)
            valid (str): Valid characters, defaults to string.printable

        Returns:
            str: clean text
        """
        clean_version = ""
        if text:
            for letter in text:
                if letter in valid:
                    clean_version += letter
        return clean_version

    @staticmethod
    def safe_to_text(
        the_value: Any,
        the_default: str,
        valid: str = string.printable,
    ) -> str:
        """
        Convert to string, but make the text safe

        Args:
            the_value (Any): (sic)
            the_default (str): (sic)
            valid: (str): valid characters

        Returns:
            str: clean string
        """
        return_value = the_default
        try:
            return_value = str(the_value)
        except:  # noqa: E722 # pragma: no cover
            return_value = the_default
        return ConvertHelpers.clean_text(return_value, valid)
