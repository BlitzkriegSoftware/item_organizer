class DatabaseException(Exception):
    def __init__(self, message, query: str):
        super().__init__(message)
        self.query = query
        self.message = message

    def __str__(self):
        return f"{self.query} - {self.message}"
