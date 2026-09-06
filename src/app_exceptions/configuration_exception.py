class ConfigurationException(Exception):
    def __init__(self, message, config_key: str, config_source: str = "env"):
        super().__init__(message)
        self.config_key = config_key
        self.config_source = config_source
        self.message = message

    def __str__(self):
        return f"[{self.config_source}] {self.config_key} - {self.message}"
