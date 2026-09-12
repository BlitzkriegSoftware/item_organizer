from collections.abc import MutableMapping

from varname import nameof

from app_logger.applogger import AppLogger


def test_logger_maker():
    logger = AppLogger.logger_get(nameof(test_logger_maker))
    assert logger is not None

def test_logger_debug():
    AppLogger.log_debug("Debug message from PyTest", logger_name=nameof(test_logger_debug))
    
def test_logger_info():
    test_extra: MutableMapping[str, object] = {
        "test_key": "test_value"
    }
    AppLogger.log_info("Info message from PyTest",test_extra,logger_name=nameof(test_logger_info))

def test_logger_exception():
    test_extra: MutableMapping[str, object] = {
        "test_key": "test_value"
    }
    try:
        raise ValueError("Test exception")
    except Exception as ex:
        AppLogger.log_exception("q", ex, test_extra, logger_name=nameof(test_logger_exception))

def test_logger_fatal():
    configurationKey = "env:TEST_CONFIG_KEY"
    test_extra: MutableMapping[str, object] = {
        "test_key": "test_value"
    }
    AppLogger.log_fatal("q", configurationKey, test_extra, logger_name=nameof(test_logger_fatal))

def test_logger_exception_no_extra():
    try:
        raise ValueError("Test exception")
    except Exception as ex:
        AppLogger.log_exception("q", ex, logger_name=nameof(test_logger_exception_no_extra))

def test_logger_info_no_extra():
    AppLogger.log_info("Info message from PyTest", logger_name=nameof(test_logger_info_no_extra))


def test_logger_debug_no_extra():
    AppLogger.log_debug("Debug message from PyTest", logger_name=nameof(test_logger_debug_no_extra))

def test_logger_debug_extra():
    test_extra: MutableMapping[str, object] = {
        "test_key": "test_value"
    }
    AppLogger.log_debug("Debug message with extra from PyTest", test_extra, logger_name=nameof(test_logger_debug_extra))