from app_logger.applogger import AppLogger


def test_logger_maker():
    logger = AppLogger.logger_get()
    assert logger is not None

    logger.info("Hello from PyTest")
