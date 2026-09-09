class PolicyException(Exception):
    def __init__(self, message, policy: str):
        super().__init__(message)
        self.policy = policy
        self.message = message

    def __str__(self):
        return f"{self.policy} - {self.message}"
