import re


class TypeValidators:
    """
    Type Validators
    """

    @staticmethod
    def is_email(email: str) -> bool:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        result = re.fullmatch(pattern, email)
        return result is not None

    @staticmethod
    def is_url(url: str) -> bool:
        pattern = r"^(https?):\/\/([a-zA-Z0-9.-]+)(:[0-9]+)?(\/[a-zA-Z0-9._~:/?#\[\]@!$&'()*+,;=-]*)?$"
        result = re.fullmatch(pattern, url)
        return result is not None
