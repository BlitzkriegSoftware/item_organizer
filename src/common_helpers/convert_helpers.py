from typing import Any


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
        except:  # noqa: E722
            return_value = the_default
        return return_value
