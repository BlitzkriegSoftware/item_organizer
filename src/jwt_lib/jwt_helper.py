import os
from datetime import datetime, timedelta, timezone
from functools import cache
from typing import Annotated, Any

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from varname import nameof

from app_exceptions.credentials_exception import CredentialsException
from app_exceptions.validation_exception import ValidationException


class JWTHelper:
    """
    Static Method Helper for JWTs

    See: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#update-the-dependencies
    """

    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")

    @cache
    @staticmethod
    def jwt_key_get():
        return os.getenv("IOR_JWT_KEY", "")

    @staticmethod
    def seconds_from_now(in_seconds: int) -> timedelta:
        return timedelta(seconds=in_seconds)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        if not data:
            raise ValidationException("Required", nameof(data), "(empty dict)")

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode = data.copy()
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode, JWTHelper.jwt_key_get(), algorithm=JWTHelper.ALGORITHM
        )

        return encoded_jwt

    @staticmethod
    def validate_token(
        token: Annotated[str, Depends(OAUTH2_SCHEME)],
    ) -> dict[str, Any]:
        try:
            payload = jwt.decode(
                token, JWTHelper.jwt_key_get(), algorithms=[JWTHelper.ALGORITHM]
            )
        except InvalidTokenError as ex:
            payload = None
            raise CredentialsException(str(ex), 403, ex, {"token": token})

        return payload
