from typing import Any
# from varname import nameof


class ValidationException(Exception):
    def __init__(self, message, field_name: str, invalid_value: Any = None):
        """
        Validation Exception

        Args:
            message (_type_): (sic)
            field_name (str): concider: nameof(variable)
            invalid_value (Any, optional): concider: str(variabble). Defaults to None.
        """
        super().__init__(message)
        self.field_name = field_name
        self.invalid_value = invalid_value
        self.message = message

    def __str__(self):
        return f"{self.field_name}={self.invalid_value} - {self.message}"
