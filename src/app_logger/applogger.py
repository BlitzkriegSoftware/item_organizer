from functools import cache
import inspect
import os
import logging
import logging.config
from typing import MutableMapping
from pythonjsonlogger import jsonlogger
from varname import nameof  # noqa: F401


class AppLogger:
    """Provides logging helpers"""

    # 1. Define configuration using dictConfig
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,  # Keeps 3rd party logs intact
        "formatters": {
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                # Fields you want extracted into your JSON object
                "format": "%(asctime)s %(levelname)s %(name)s %(message)s %(filename)s %(lineno)d",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "json",
            },
        },
        "loggers": {
            # Root logger captures everything from app & dependencies
            "": {
                "handlers": ["console"],
                "level": os.environ.get("LOG_LEVEL", "INFO"),
            },
        },
    }

    @cache
    @staticmethod
    def logger_get(logger_name: str | None = None) -> logging.Logger:
        logging.config.dictConfig(AppLogger.LOGGING_CONFIG)
        if not logger_name:
            logger_name = __name__
        logger = logging.getLogger(logger_name)
        return logger

    @staticmethod
    def log_exception(
        query: str,
        ex: Exception,
        extra: MutableMapping[str, object] = {},
    ):
        if not query:
            query = ""
        else:
            extra[nameof(query)] = query

        if not ex:
            return
        else:
            extra[nameof(ex)] = ex

        logger = AppLogger.logger_get()
        filename, lineno, co_name, sinfo = logger.findCaller(False, 2)

        key = f"bls_{nameof(filename)}"
        if filename and key not in extra:
            extra[key] = filename

        key = f"bls_{nameof(lineno)}"
        if lineno and key not in extra:
            extra[key] = lineno

        key = f"bls_{nameof(co_name)}"
        if co_name and key not in extra:
            extra[key] = co_name

        key = f"bls_{nameof(sinfo)}"
        if sinfo and key not in extra:
            extra[key] = sinfo

        logger.exception("%s; %s", query, str(ex), extra=extra)

    @staticmethod
    def log_info(
        message: str,
        extra: MutableMapping[str, object] = {},
    ):
        if not message:
            return

        logger = AppLogger.logger_get()
        filename, lineno, co_name, sinfo = logger.findCaller(False, 2)

        key = f"bls_{nameof(filename)}"
        if filename and key not in extra:
            extra[key] = filename

        key = f"bls_{nameof(lineno)}"
        if lineno and key not in extra:
            extra[key] = lineno

        key = f"bls_{nameof(co_name)}"
        if co_name and key not in extra:
            extra[key] = co_name

        key = f"bls_{nameof(sinfo)}"
        if sinfo and key not in extra:
            extra[key] = sinfo

        logger.info(
            message,
            extra=extra,
        )
