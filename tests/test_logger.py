from applogger.applogger import configure_logging


def test_logger_maker():
    logger = configure_logging()
    assert logger is not None

    logger.info("Hello from PyTest")
