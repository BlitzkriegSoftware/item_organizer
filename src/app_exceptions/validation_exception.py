class ValidationException(Exception):
    def __init__(self, message, field_name: str):
        super().__init__(message)
        self.field_name = field_name
        self.message = message

    def __str__(self):
        return f"{self.field_name} - {self.message}"
