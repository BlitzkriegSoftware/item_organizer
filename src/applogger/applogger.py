import logging
import logging.config


def configure_logging() -> logging.Logger:
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

    # 2. Apply configuration
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)
    return logger
