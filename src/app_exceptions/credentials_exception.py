class CredentialsException(Exception):
    def __init__(
        self,
        message,
        http_status_code: int,
        inner_exception,
        info: dict[str, str] = {},
    ):
        super().__init__(message)
        self.message = message
        self.http_status_code = http_status_code
        self.info = info
        self.inner_exception = inner_exception

    def __str__(self):
        return f"{self.http_status_code}: {self.message}\n{self.info}\n{self.inner_exception}"


# credentials_exception = HTTPException(
#     status_code=status.HTTP_401_UNAUTHORIZED,
#     detail="Could not validate credentials",
#     headers={"WWW-Authenticate": "Bearer"},
# )
