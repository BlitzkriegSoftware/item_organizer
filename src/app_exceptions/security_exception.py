class SecurityException(Exception):
    def __init__(self, message, context: str):
        super().__init__(message)
        self.context = context
        self.message = message

    def __str__(self):
        return f"{self.context} - {self.message}"
