from varname import nameof

from app_logger.applogger import AppLogger


def test_logger_maker():
    logger = AppLogger.logger_get(nameof(test_logger_maker))
    assert logger is not None

    logger.info("Hello from PyTest")
