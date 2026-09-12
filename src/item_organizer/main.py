from varname import nameof

from app_logger.applogger import AppLogger


def main(): # pragma: no cover
    message: str = "item-organizer start up"
    logger = AppLogger.logger_get(nameof(main))
    logger.info(message)
    print(message)


if __name__ == "__main__": # pragma: no cover
    main()
